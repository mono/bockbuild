class MonoUpnpPackage (GitHubTarballPackage):
	def __init__ (self):
		GitHubTarballPackage.__init__ (self, 'mono', 'mono-upnp',
			'0.1.2', 'b374ed41c566bc6ad50b3513218458b711e508db',
			configure = './autogen.sh --prefix="%{prefix}"')

		self.configure_flags = [
			'--disable-tests',
		]

		self.sources.extend ([
			# allow building without NUnit installed
			'patches/mono-upnp_add_disable_tests_flag.patch'
		])

	def prep (self):
		GitHubTarballPackage.prep (self)
		for p in range (1, len (self.sources)):
			self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

MonoUpnpPackage ()
