class GtkOSXDocbookPackage (GitHubTarballPackage):
	def __init__ (self):
		GitHubTarballPackage.__init__ (self, 'jralls', 'gtk-osx-docbook',
			'1.0', '058d8a2f3f0d37de00b8e9ac78f633706deb5e22', '')

	def build (self):
		return

	def install (self):
		self.sh ('JHBUILD_PREFIX="%{prefix}" %{makeinstall}')


GtkOSXDocbookPackage ()
