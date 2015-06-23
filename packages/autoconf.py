class Autoconf (GnuPackage):
	def __init__ (self):
		GnuPackage.__init__ (self, 'autoconf', '2.69', override_properties = { 'build_dependency' : True })
		self.extra_stage_files = ['share/autoconf/autom4te.cfg']

	def build (self):
		pass

	def install (self):
		Package.build (self)
		Package.install (self)

		#second build, to be bundled with the package
		self.package_prefix = self.profile.prefix
		self.stage_root = self.profile.stage_root
		self.makeinstall = 'make install DESTDIR=%{stage_root}'
		Package.build (self)
		Package.install (self)

		self.stage (self.profile.staged_prefix)

Autoconf()

