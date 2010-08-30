class LibsoupPackage (GnomePackage):
	def __init__ (self):
		GnomePackage.__init__ (self, 'libsoup', '2.30', '2')
		self.configure_flags = [
			'--disable-gtk-doc',
			' --without-gnome'
		]

LibsoupPackage ()
