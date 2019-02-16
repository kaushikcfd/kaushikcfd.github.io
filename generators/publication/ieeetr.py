import bibtexparser
import sys
import re
from mako.template import Template

_MY_FIRST_NAME = 'Kaushik'
_MY_LAST_NAME = 'Kulkarni'

filename = sys.argv[1]

with open(filename) as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)


ieee_str = ""

for i, entry in enumerate(bib_database.entries):

    # getting the author pattern for IEEE
    authors = [x.strip() for x in entry['author'].split("and")]
    author_str = ""
    for author in authors:
        last_name, first_name = [x.strip() for x in author.split(", ")]
        if last_name == _MY_LAST_NAME and first_name == _MY_FIRST_NAME:
            # emphasize my name
            author_str += "**"+first_name[0]+". "+last_name+"**, "
        else:
            author_str += first_name[0]+". "+last_name+", "
    author_str = author_str[:-2]

    ieee_str += ('<ref> {authors}, "{title}," _{journal}_, vol. {vol}, '
                 'pp.{pages}, {year}.</ref>\n').format(
                        authors=author_str,
                        title=entry['title'],
                        journal=entry['journal'],
                        vol=entry['volume'],
                        pages=entry['pages'],
                        year=entry['year'])

final_str = (r"""
        ---
        title: Publications
        ...

        ${ieee_style_publications}

        ---
        <div id="footer">
        _Maintained with the help of [bibtexparser](
        https://github.com/sciunto-org/python-bibtexparser)._
        </div>

        """)

final_str = re.sub("\\n        ", "\n", final_str)

print(Template(final_str).render(
    ieee_style_publications=ieee_str))
