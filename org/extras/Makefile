all: resume

resume:
	latexmk -shell-escape -bibtex -f -pdf resume.tex

clean:
	latexmk -c && rm resume.bbl resume.run.xml
