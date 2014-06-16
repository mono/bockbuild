class FontConfigPackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'fontconfig', '2.10.2',
			configure_flags = [ '--disable-docs' ],
			sources = [
				'http://www.fontconfig.org/release/%{name}-%{version}.tar.gz'
			])

	def build (self):
		if Package.profile.name == 'darwin':
			self.configure_flags.extend ([
				'--with-default-fonts=/System/Library/Fonts',
				'--with-add-fonts=/Library/Fonts,/Network/Library/Fonts,/System/Library/Fonts'
			])
		Package.build (self)

FontConfigPackage ()
