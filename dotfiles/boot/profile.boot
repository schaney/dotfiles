(set-env! :dependencies '[[nrepl "0.6.0"]
                          [cider/cider-nrepl "0.21.1"]])

(require '[cider.tasks :refer [add-middleware nrepl-server]])

(task-options! add-middleware {:middleware '[cider.nrepl.middleware.apropos/wrap-apropos
                                             cider.nrepl.middleware.version/wrap-version]})

(def boot-version
  (get (boot.App/config) "BOOT_VERSION" "2.8.2"))

(deftask cider
  []
  (comp (add-middleware)
        (nrepl-server)
        (wait)))
