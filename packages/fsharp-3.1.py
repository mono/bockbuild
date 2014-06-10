
class Fsharp31Package(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'fsharp', 'fsharp',
			'3.1.1.14',
			'81c94470de1587902a20f40741388e361dc09690',
			configure = '')

	def build(self):
		self.sh ('autoreconf')
		self.sh ('./configure --prefix="%{prefix}"')
		self.sh ('make')

Fsharp31Package()
