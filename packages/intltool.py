class IntltoolPackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'intltool', '0.50.2',
			sources = [
				'https://launchpad.net/%{name}/trunk/%{version}/+download/%{name}-%{version}.tar.gz'
			]
		)

	def install (self):
		Package.install (self)
		intltoolize = os.path.join (self.staged_prefix, 'bin', 'intltoolize')
		Package.stage_file (self, intltoolize)

IntltoolPackage ()
