
class NuGetPackage(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'mono', 'nuget',
			'2.8.1',
			'a3941ea07d84d4bf86ab1b7678d5ae6f60f355b7',
			configure = '')

	def build(self):
		self.sh ('%{make}')

	def install(self):
		self.sh ('%{makeinstall} PREFIX=%{prefix}')

NuGetPackage()
