class FsharpPackage(GitHubTarballPackage):

    def __init__(self):
        GitHubTarballPackage.__init__(self,
                                      'fsharp', 'fsharp',
                                      '4.0.1.1',
                                      '849e3061fd7db397f07c7bd0c08e5df19f2b712a',
                                      configure='./configure --prefix="%{package_prefix}"')

        self.extra_stage_files = [
            'lib/mono/xbuild/Microsoft/VisualStudio/v/FSharp/Microsoft.FSharp.Targets']

    def build(self):
        self.sh('autoreconf')
        Package.configure(self)
        Package.make(self)

FsharpPackage()
