
class Fsharp31Package(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'fsharp', 'fsharp',
			'3.1.1.5',
			'da9d13ce525adfaa2577ea956f22bc5fed8dfb9',
			configure = '')

	def build(self):
		self.sh ('autoreconf')
		self.sh ('./configure --prefix="%{prefix}"')
		self.sh ('make')

Fsharp31Package()
