class GtkPackage (GnomePackage):
	def __init__ (self):
		GnomePackage.__init__ (self, 'gtk+',
			version_major = '2.22',
			version_minor = '0',
			configure_flags = [
				'--with-gdktarget=%{gdk_target}',
				'--disable-cups',
				'--without-libjasper'
			]
		)

		self.gdk_target = 'x11'
		if Package.profile.name == 'darwin':
			self.gdk_target = 'quartz'
			self.sources.extend ([
				'http://github.com/jralls/gtk-osx-build/raw/master/patches/gdk-quartz-input-window.patch',
				'http://git.dronelabs.com/gtk+/patch/?id=729cbea7a2b27c4b8f2062316c0f406ab4c01dac'
			])

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (2, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

GtkPackage ()
