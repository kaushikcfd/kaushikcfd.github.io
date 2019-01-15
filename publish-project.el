(package-initialize)
(require 'org)
(require 'ox)
(require 'ox-publish)

(setq org-html-postamble-format 
       '(("en" "<p class=\"date\">Last Updated %T.</p>
                <p class=\"creator\">Created using %c</p>")))

(setq org-publish-project-alist
    '(
      ;; org files to be exported to HTML.
      ("org"
       :author "Kaushik Kulkarni"
       :base-directory "./org"
       :base-extension "org"
       :publishing-directory "./html"
       :publishing-function org-html-publish-to-html
       :section-numbers nil
       :with-toc nil
       :html-extension "html"
       :html-head-include-scripts nil
       :html-html5-fancy t
       :html-doctype "html5"
       :html-postamble t
       :recursive t)

      ;; CSS files to be copied to the html folder.
      ("css"
       :base-directory "./org/css"
       :base-extension "css"
       :publishing-directory "./html/css"
       :publishing-function org-publish-attachment)

      ;; Extra files to be copied to the html folder.
      ("extras"
       :base-directory "./org/extras"
       :base-extension "pdf"
       :publishing-directory "./html/extras"
       :publishing-function org-publish-attachment)

      ;; Publish all of the components in order.
      ("personal-webpage" :components ("org" "css" "extras"))
    )
)
