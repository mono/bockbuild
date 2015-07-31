class FsharpPackage(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'fsharp', 'fsharp',
			'4.0.0.1',
			'c3aaf7d5f1f8905bbb3522b327703a43a0842cdf',
			configure = './configure --prefix="%{package_prefix}"')
		self.sources.extend ([
			'patches/fsharp-fix-net45-profile.patch'])

		self.extra_stage_files = ['lib/mono/xbuild/Microsoft/VisualStudio/v/FSharp/Microsoft.FSharp.Targets']

	def prep(self):
		Package.prep (self)

		for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{local_sources[' + str (p) + ']}"')


	def build(self):
		self.sh ('autoreconf')
		Package.configure (self)
		Package.make (self)

FsharpPackage()