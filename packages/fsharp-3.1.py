
class Fsharp31Package(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'fsharp', 'fsharp',
			'3.1.1.27',
			'128f3bc8daf02fcd44724d7999252a1c8cc0e73c',
			configure = '')

	def build(self):
		self.sh ('autoreconf')
		self.sh ('./configure --prefix="%{prefix}"')
		self.sh ('make')

Fsharp31Package()
