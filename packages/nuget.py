
class NuGetPackage(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'mono', 'nuget',
			'2.8.1',
			'02b1ac03c36cb014e1c2d3d2c47b6992d15b413b',
			configure = '')

	def build(self):
		self.sh ('%{make} PREFIX=%{prefix}')

	def install(self):
		self.sh ('%{makeinstall} PREFIX=%{prefix}')

NuGetPackage()
