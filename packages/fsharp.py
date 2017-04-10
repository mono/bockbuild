class FsharpPackage(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'fsharp', 'fsharp',
			'4.1.8',
			'29607f57efe83edeecd35070929fbdcf001b4d37',
			configure = './configure --prefix="%{package_prefix}"',
			override_properties = { 'make': 'make' })

		self.extra_stage_files = ['lib/mono/xbuild/Microsoft/VisualStudio/v/FSharp/Microsoft.FSharp.Targets']
		self.sources.extend ([
			'patches/fsharp-fix-mdb-support.patch',
			'patches/fsharp-fix-compile-after-issue.patch',
			'patches/fsharp-Add-missing-symlinks.patch'])

	def prep(self):
		Package.prep (self)

		for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{local_sources[' + str (p) + ']}"')

	def build(self):
		self.sh ('autoreconf')
		Package.configure (self)
		Package.make (self)

FsharpPackage()
