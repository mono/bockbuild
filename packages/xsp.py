class XspPackage (GitHubTarballPackage):
	def __init__ (self):
		GitHubTarballPackage.__init__ (self, 'mono', 'xsp', '3.0.11',
			'e272a2c006211b6b03be2ef5bbb9e3f8fefd0768',
			 configure = './autogen.sh --prefix="%{staged_prefix}"')
		self.makeinstall = 'make install'

XspPackage ()
