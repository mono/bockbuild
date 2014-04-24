
class NuGetPackage(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'mono', 'nuget',
			'2.8.1',
			'2e0253dcf62ce4d084f7f5c8b0f5f663b70a4b60',
			configure = '')

	def build(self):
		self.sh ('%{make}')

	def install(self):
		self.sh ('%{makeinstall} PREFIX=%{prefix}')

NuGetPackage()
