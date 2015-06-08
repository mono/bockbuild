
class Fsharp31Package(GitHubTarballPackage):

    def __init__(self):
        GitHubTarballPackage.__init__(self,
                                      'fsharp', 'fsharp',
                                      '3.1.1.31',
                                      '1f79c0455fb8b5ec816985f922413894ce19359a',
                                      configure='./configure --prefix="%{package_prefix}"')
        self.sources.extend([
            'patches/fsharp-fix-net45-profile.patch'])

    def prep(self):
        Package.prep(self)

        for p in range(1, len(self.sources)):
            self.sh('patch -p1 < "%{local_sources[' + str(p) + ']}"')

    def build(self):
        self.sh('autoreconf')
        Package.configure(self)
        Package.make(self)

Fsharp31Package()
