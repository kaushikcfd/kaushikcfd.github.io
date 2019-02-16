all: generators html

generators: publications

publications: org/extras/publications.bib
	python generators/publication/ieeetr.py org/extras/publications.bib > org/publications.html

html: org/index.org
	emacs --batch --load publish-minipage.el --eval '(org-publish "personal-webpage" t)'

remove-temps:
	find -L . -name '*~' | xargs rm
