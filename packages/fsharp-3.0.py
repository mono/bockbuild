
class FsharpPackage(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'fsharp', 'fsharp',
			'3.0.31',
			'b00fa1d2c0de85b21590a5b32527031df8ececf5',
			configure = '')

	def build(self):
		self.sh ('autoreconf')
		self.sh ('./configure --prefix="%{prefix}"')
		self.sh ('make')

FsharpPackage()
