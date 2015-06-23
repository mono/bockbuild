class Automake (GnuPackage):
	def __init__ (self):
		GnuPackage.__init__ (self, 'automake', '1.13', override_properties = { 'build_dependency' : True })
		self.verbose = True
		self.extra_stage_files = ['share/automake-%{version}/Automake/Config.pm']

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

Automake()
