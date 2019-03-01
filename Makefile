all: html

html: org/index.org generators
	emacs --batch --load publish-minipage.el --eval '(org-publish "personal-webpage" t)'

generators: publications

publications: org/extras/journal.bib org/extras/conference.bib
	python generators/publication/ieeetr.py --fname org/extras/journal.bib --heading 'Publication(s)' > org/publications.html
	python generators/publication/ieeetr.py --fname org/extras/conference.bib --heading 'Talk(s)' > org/talks.html

remove-temps:
	find -L . -name '*~' | xargs rm
