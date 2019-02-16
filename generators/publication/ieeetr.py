import bibtexparser
import sys
import re
import datetime
from mako.template import Template

filename = sys.argv[1]

with open(filename) as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)


ieee_str = ""

for i, entry in enumerate(bib_database.entries):

    # getting the author pattern for IEEE
    authors = [x.strip() for x in entry['author'].split("and")]
    author_str = ""
    for author in authors:
        strongify = False
        if author[:8] == r'\textbf{':
            #FIXME: use regex here
            author = author[8:-1]
            strongify = True
        last_name, first_name = [x.strip() for x in author.split(", ")]
        if strongify:
            author_str += "<strong>{0}. {1}</strong>, ".format(
                    first_name[0], last_name)
        else:
            author_str += "{0}. {1}, ".format(first_name[0], last_name)

    author_str = author_str[:-2]

    ieee_str += ('<ref> {authors}, &ldquo;{title},&rdquo; <em>{journal}</em>, '
                 'vol. {vol}, pp.{pages}, {year}.</ref>\n').format(
                        authors=author_str,
                        title=entry['title'],
                        journal=entry['journal'],
                        vol=entry['volume'],
                        pages=entry['pages'],
                        year=entry['year'])

final_str = (r"""
        <!DOCTYPE html>
        <html>
        <head>
        <link rel="stylesheet" type="text/css" href="css/style.css"/>
        </head>
        <body>

        <h1>Publications</h1>


        ${ieee_style_publications}


        <hr >
        <div id="postamble" class="status">
        <p class="creator">Last Updated ${year}-${month}-${date}.</br>Maintained
        with the help of
        <a href="http://github.com/sciunto-org/python-bibtexparser/">bibtexparser</a>
        </p>
        </div>
        </body>
        </html>

        """)

final_str = re.sub("\\n        ", "\n", final_str)

print(Template(final_str).render(
    ieee_style_publications=ieee_str,
    date=datetime.date.today().strftime("%d"),
    month=datetime.date.today().strftime("%m"),
    year=datetime.date.today().strftime("%Y")))
