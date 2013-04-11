
class FsharpPackage(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'fsharp', 'fsharp',
			'3.0.27',
			'f3c8ea8bf4831ce6dc30581558fa4a45a078cd55',
			configure = '')

	def build(self):
		self.sh ('autoreconf')
		self.sh ('./configure --prefix="%{prefix}"')
		self.sh ('make')

FsharpPackage()
