
class Fsharp30Package(GitHubTarballPackage):

    def __init__(self):
        GitHubTarballPackage.__init__(self,
                                      'fsharp', 'fsharp',
                                      '3.0.34',
                                      'b0c16bb496fbc4df88b56957efc70c80c8624d2d',
                                      configure='')

    def build(self):
        self.sh('autoreconf')
        self.sh('./configure --prefix="%{prefix}"')
        self.sh('make')

Fsharp30Package()
