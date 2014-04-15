
class NuGetPackage(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'mono', 'nuget',
			'2.8.1',
			'8466c6d912d0b03726c3c025a8eaf9397bdd30c3',
			configure = '')

	def build(self):
		self.sh ('%{make}')

	def install(self):
		self.sh ('%{makeinstall} PREFIX=%{prefix}')

NuGetPackage()
