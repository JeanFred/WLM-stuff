#!/usr/bin/python
# -=- encoding: utf-8 -=-

"""Add custom identifiers to CH monuments without one."""

import pywikibot as wikipedia
from pywikibot import pagegenerators
from pywikibot import textlib
import re
import argparse


KGS_re = re.compile(r"""
    KGS-Nr
    \s*?           # Maybe some whitespace
    =              # Equal sign
    \s*?           # Maybe some whitespace
    (?P<id>.+?)    # Something, captured as id
    \s*?           # Maybe some whitespace
    \|             # A pipe
    """, re.VERBOSE)

id_counter = 0


def list_template_usage(row_template_name):
    """Return a generator of main space pages transcluding a given template."""
    site = wikipedia.getSite('de', 'wikipedia')
    rowTemplate = wikipedia.Page(site, u'%s:%s' % (site.namespace(10), row_template_name))
    transGen = pagegenerators.ReferringPageGenerator(rowTemplate, onlyTemplateInclusion=True)
    filteredGen = pagegenerators.NamespaceFilterPageGenerator(transGen, [0])
    generator = pagegenerators.PreloadingGenerator(filteredGen)
    return generator


def process_page_contents(page_contents):
    """Return the processed contents of a page."""
    output = []
    global id_counter
    for line in page_contents.split('\n'):
        KGS_match = re.search(KGS_re, line)
        if KGS_match:
            id = KGS_match.group('id').strip()
            if id == '?' or id == '':
                id_counter += 1
                identifier = "wlmch-missing-%s" % id_counter
                line2 = KGS_re.sub(r'KGS-Nr = %s |' % identifier, line)
                output.append(line2)
            else:
                output.append(line)
        else:
            output.append(line)
    return '\n'.join(output)


def run():
    """Run the ID generation / replacement script."""
    generator = list_template_usage('Denkmalliste Schweiz Tabellenzeile')
    for page in generator:
        if page.exists() and not page.isRedirectPage():
            contents = page.get()
            permalink = page.permalink()
            print permalink
            print process_page_contents(contents)


def main():
    """Main method."""
    desc = "Add custom identifiers to CH monuments without one."
    parser = argparse.ArgumentParser(description=desc)
    args = parser.parse_args()
    run()


if __name__ == '__main__':
    main()
