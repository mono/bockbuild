
class NuGetPackage(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'mono', 'nuget',
			'2.8.5',
			'ea1d244b066338c9408646afdcf8acae6299f7fb',
			configure = '')

	def build(self):
		self.sh ('%{make} PREFIX=%{prefix}')

	def install(self):
		self.sh ('%{makeinstall} PREFIX=%{prefix}')

NuGetPackage()
