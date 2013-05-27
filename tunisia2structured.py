#!/usr/bin/python
# -=- encoding: utf-8 -=-

"""Convert a Tunisian monuments list to structured format."""

import re
import sys
import argparse

scope_re = re.compile(r"""
    ^\s!\s         # Starts with whitespace and a !
    scope=\"row\"  #
    \s\|\s         # Whitespace, pipe, whitespace
    (?P<id>\d*)    # digits, captured as id
    \s*$           # Whitespace until the end
    """, re.VERBOSE)


def parse_tunisia_list(f, iso_code):
    """Parse the given list and return each row in template format."""
    id = None
    for line in f:
        if line == "":
            continue
        elif line.startswith(' |----'):
            continue
        else:
            scope_match = re.search(scope_re, line)
            if scope_match:
                id = scope_match.group('id')
            else:
                headers = ['site', 'monument', 'image',
                           'date', 'decret', 'coord']
                array = line.strip(' | ').strip('\n').split('||')
                array = [x.strip() for x in array]
                mydict = dict(zip(headers, array))
                mydict['iso'] = iso_code
                mydict['id'] = id
                yield make_template(**mydict)


def make_template(**kwargs):
    """Convert a Tunisian monuments list to structured format"""
    return """\
{{{{Ligne de tableau monument Tunisie
|id={iso}-{id}
|site={site}
|monument={monument}
|adresse=
|date={date}
|decret={decret}
|coordinates={coord}
|image={image}
}}}}""".format(**kwargs)


def make_article_text(iso, text):
    """Make a stub article."""
    return """\
Cet article recense les [[Monument historique|monuments historiques]] et \
archéologiques protégés et classés du [[gouvernorat de l'Ariana]], établie \
par l'[[Institut national du patrimoine (Tunisie)|Institut national du patrimoine]].

== Liste ==

{{En-tête de tableau monument Tunisie|gouvernat_iso=TN-%s}}
%s
|}

== Voir aussi ==

=== Article connexe ===
*[[Liste des monuments classés de Tunisie]]

=== Lien externe ===
*{{KML}}

{{Portail|Protection du patrimoine|archéologie|Tunisie}}

[[Catégorie:Liste de monuments classés de Tunisie]]
""" % (iso, text)


def convert_list(handle, iso_code):
    """Convert a given list to article."""
    text = "\n".join(list(parse_tunisia_list(handle, iso_code)))
    return make_article_text(iso_code, text)


def main():
    """Main method."""
    desc = "Converts Tunisia unstructured list to structured lists."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--list', dest="list_file", type=file,
                        required=True,
                        help='The text file with the wikicode')
    parser.add_argument('--iso', dest="iso_code", type=int,
                        required=True,
                        help='The ISO code of the gouvernat.')
    args = parser.parse_args()
    print convert_list(args.list_file, args.iso_code)


if __name__ == '__main__':
    main()
