class BansheePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'banshee-1', '1.5.4')

		self.sources = [
			'http://download.banshee-project.org/banshee/stable/%{version}/%{name}-%{version}.tar.bz2'
		]

		self.configure_flags = [
			'--disable-docs',
			'--disable-webkit'
		]

		if Package.profile.name == 'darwin':
			self.configure_flags.extend ([
				'--disable-mtp',
				'--disable-daap',
				'--disable-ipod',
				'--disable-boo',
				'--disable-gnome',
				'--enable-osx',
				'--with-vendor-build-id="banshee-project.org OSX 10.5+ i386/Intel"'
			])

BansheePackage ()
