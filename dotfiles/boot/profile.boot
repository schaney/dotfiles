(deftask cider "CIDER profile"
  []
  (require 'boot.repl)
  (swap! @(resolve 'boot.repl/*default-dependencies*)
         concat '[[org.clojure/tools.nrepl "0.2.12"]
                  [cider/cider-nrepl "0.15.0-SNAPSHOT"]
                  [refactor-nrepl "2.3.0-SNAPSHOT"]])
  (swap! @(resolve 'boot.repl/*default-middleware*)
         concat '[cider.nrepl/cider-middleware
                  refactor-nrepl.middleware/wrap-refactor])
  identity)

(def boot-version
  (get (boot.App/config) "BOOT_VERSION" "2.7.1"))

(deftask from-lein
  "Use project.clj as source of truth as far as possible"
  []
  (let [lein-proj (let [l (-> "project.clj" slurp read-string)]
                    (merge (->> l (drop 3) (partition 2) (map vec) (into {}))
                           {:project (second l) :version (nth l 2)}))]
    (merge-env! :repositories (:repositories lein-proj))
    (set-env!
      :certificates   (:certificates lein-proj)
      :source-paths   (or (:source-paths lein-proj) #{"src"})
      :resource-paths (or (:resource-paths lein-proj) #{"resources"})
      :dependencies   (into (:dependencies lein-proj)
                            `[[boot/core ~boot-version   :scope "provided"]
                              [adzerk/bootlaces "0.1.13" :scope "test"]]))

    (require '[adzerk.bootlaces :refer :all])
    ((resolve 'bootlaces!) (:version lein-proj))
    (task-options!
      repl (:repl-options lein-proj {})
      aot  (let [aot (:aot lein-proj)
                 all? (or (nil? aot) (= :all aot))
                 ns (when-not all? (set aot))]
             {:namespace ns :all all?})
      jar  {:main (:main lein-proj)}
      pom  {:project     (symbol (:project lein-proj))
            :version     (:version lein-proj)
            :description (:description lein-proj)
            :url         (:url lein-proj)
            :scm         (:scm lein-proj)
            :license     (get lein-proj :license {"EPL" "http://www.eclipse.org/legal/epl-v10.html"})}))
  identity)
