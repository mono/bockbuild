class LibXmlPackage (Package):
	def __init__ (self):
		Package.__init__ (self,
			'libxml2',
			'2.9.1',
			configure_flags = [ '--with-python=no' ],
			sources = [
				'ftp://xmlsoft.org/%{name}/%{name}-%{version}.tar.gz',
			]
		)

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in self.patches:
				p.run(self)

LibXmlPackage ()

