class MSTestSuitePackage(GitHubPackage):
    def __init__(self):
        Package.__init__(self,
                         name='ms-test-suite',
                         version='0.1',
                         organization='xamarin',
                         sources=['git@github.com:xamarin/ms-test-suite.git'])

    def namever (self):
        return "ms-test-suite"

    def prep(self):
        pass
    def build(self):
        pass
    def install(self):
        # self.sh ("cd %s/ms-test-suite/conformance; make build && make run || true" % (self.package_build_dir()))

MSTestSuitePackage()
