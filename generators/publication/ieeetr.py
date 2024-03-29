import bibtexparser
import re
import datetime
import argparse
from mako.template import Template
from bibtexparser.bparser import BibTexParser


parser = argparse.ArgumentParser()
parser.add_argument('--fname', dest='fname', type=str)
parser.add_argument('--heading', dest='heading', type=str)

args, _ = parser.parse_known_args()
filename = args.fname
heading = args.heading

with open(filename) as bibtex_file:
    bib_parser = BibTexParser(ignore_nonstandard_types=False)
    bib_database = bibtexparser.load(bibtex_file, bib_parser)


ieee_str = ""

for i, entry in enumerate(bib_database.entries):
    authors = [x.strip() for x in entry['author'].split("and")]
    author_str = ""
    for author in authors:
        last_name, first_name = [x.strip() for x in author.split(", ")]
        author_str += "{0}. {1}, ".format(first_name[0], last_name)

    author_str = author_str[:-2]
    title = re.sub("[{}]", "", entry["title"])

    if entry['ENTRYTYPE'] == 'article':
        ieee_str += ('<ref> {authors}, &ldquo;{title},&rdquo; <em>{journal}</em>, '
                     'vol. {vol}, pp.{pages}, {year}.</ref>\n').format(
                            authors=author_str,
                            title=title,
                            journal=entry['journal'],
                            vol=entry['volume'],
                            pages=entry['pages'],
                            year=entry['year'])
    elif entry['ENTRYTYPE'] == 'preprint':
        ieee_str += ('<ref> {authors}, &ldquo;{title},&rdquo; <em>{journal}</em>, '
                     '{year}.</ref>\n').format(
                            authors=author_str,
                            title=title,
                            journal=entry['journal'],
                            year=entry['year'])
    elif entry['ENTRYTYPE'] == 'inproceedings':
        if 'series' in entry:
            ieee_str += ('<ref> {authors}, &ldquo;{title},&rdquo; ser. '
                    '<em>{series}</em>, {pub}, {year}.</ref>\n').format(
                            authors=author_str,
                            title=title,
                            series=entry['series'],
                            pub=entry['publisher'],
                            year=entry['year'])
        else:
            ieee_str += ('<ref> {authors}, &ldquo;{title},&rdquo;'
                    ', {pub}, {year}.</ref>\n').format(
                            authors=author_str,
                            title=title,
                            pub=entry['publisher'],
                            year=entry['year'])
    else:
        raise NotImplementedError()

# deal with umlauts
ieee_str = re.sub(r'\\"{o}', r'ö', ieee_str)
# {{sometext}} => sometext
ieee_str = re.sub(r'{{(.*)}}', '\g<1>', ieee_str)

final_str = (r"""
        <!DOCTYPE html>
        <html>
        <head>
        <link rel="stylesheet" type="text/css" href="css/style.css"/>
        </head>
        <body>

        <h1>${heading}</h1>


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
    heading=heading,
    ieee_style_publications=ieee_str,
    date=datetime.date.today().strftime("%d"),
    month=datetime.date.today().strftime("%m"),
    year=datetime.date.today().strftime("%Y")))
