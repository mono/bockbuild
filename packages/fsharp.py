class FsharpPackage(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'fsharp', 'fsharp',
			'4.0.0.3',
			'14db8f5c19814dad05f51cf08e7ca718404e0e0a',
			configure = './configure --prefix="%{package_prefix}"')

		self.extra_stage_files = ['lib/mono/xbuild/Microsoft/VisualStudio/v/FSharp/Microsoft.FSharp.Targets']
		self.sources.extend (['patches/fsharp-el-capitan-fix.patch']) # https://github.com/fsharp/fsharp/pull/495

	def prep(self):
		Package.prep (self)

		for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{local_sources[' + str (p) + ']}"')

	def build(self):
		self.sh ('autoreconf')
		Package.configure (self)
		Package.make (self)

FsharpPackage()