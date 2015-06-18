
class Fsharp31Package(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'fsharp', 'fsharp',
			'3.1.1.31',
			'1f79c0455fb8b5ec816985f922413894ce19359a',
			configure = './configure --prefix="%{package_prefix}"')
		self.sources.extend ([
			Patch ('patches/fsharp-fix-net45-profile.patch', options = '-p1')
		])

	def prep(self):
		Package.prep (self)

		for p in self.patches:
			p.run (self)


	def build(self):
		self.sh ('autoreconf')
		Package.configure (self)
		Package.make (self)

Fsharp31Package()
