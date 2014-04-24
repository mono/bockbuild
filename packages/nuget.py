
class NuGetPackage(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'mono', 'nuget',
			'2.8.1',
			'7b20cd5408852e725bd14a13855bd238506c6a19',
			configure = '')

	def build(self):
		self.sh ('%{make}')

	def install(self):
		self.sh ('%{makeinstall} PREFIX=%{prefix}')

NuGetPackage()
