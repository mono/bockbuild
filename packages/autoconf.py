class Autoconf (GnuPackage):
	def __init__ (self):
		GnuPackage.__init__ (self, 'autoconf', '2.69', override_properties = { 'build_dependency' : True })

	def build (self):
		pass

	def install (self):
		Package.build (self)
		Package.install (self)

		#second build, to be bundled with the package
		self.package_prefix = self.profile.prefix
		self.makeinstall = 'make install DESTDIR=%{stage_root}'
		Package.build (self)
		Package.install (self)

Autoconf()

