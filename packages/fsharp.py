class FsharpPackage(GitHubTarballPackage):

    def __init__(self):
        GitHubTarballPackage.__init__(self,
                                      'fsharp', 'fsharp',
                                      '4.0.1.1',
                                      '849e3061fd7db397f07c7bd0c08e5df19f2b712a',
                                      configure='./configure --prefix="%{package_prefix}"')

        self.extra_stage_files = [
            'lib/mono/xbuild/Microsoft/VisualStudio/v/FSharp/Microsoft.FSharp.Targets']
        self.sources.extend(['patches/fsharp-assemblysearchpath-fix.patch']) # https://github.com/fsharp/fsharp/pull/596

    def prep(self):
        Package.prep(self)

        for p in range(1, len(self.sources)):
            self.sh('patch -p1 < "%{local_sources[' + str (p) + ']}"')

    def build(self):
        self.sh('autoreconf')
        Package.configure(self)
        Package.make(self)

FsharpPackage()
