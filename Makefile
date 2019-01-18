all:
	emacs --batch --load publish-minipage.el --eval '(org-publish "personal-webpage" t)'

remove-temps:
	find -L . -name '*~' | xargs rm
