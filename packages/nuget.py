
class NuGetPackage(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'mono', 'nuget',
			'2.8.1',
			'b6e48bb34e63d33327330cbe8cdd92a4d9afd30d',
			configure = '')

	def build(self):
		self.sh ('%{make}')

	def install(self):
		self.sh ('%{makeinstall} PREFIX=%{prefix}')

NuGetPackage()
