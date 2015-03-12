
class Fsharp31Package(GitHubTarballPackage):
	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'fsharp', 'fsharp',
			'3.1.1.28',
			'ce0ba4e7c63ceda9df244e9a2bac196eecad1e80',
			configure = './configure --prefix="%{package_prefix}"')

	def build(self):
		self.sh ('autoreconf')
		Package.configure (self)
		Package.make (self)

Fsharp31Package()
