class GtkPackage (GnomePackage):
	def __init__ (self):
		GnomePackage.__init__ (self, 'gtk+',
			version_major = '2.18',
			version_minor = '5',
			configure_flags = [
				'--with-gdktarget=%{gdk_target}',
				'--disable-cups',
				'--without-libjasper',
				'--without-libtiff'
			]
		)

		if Package.profile.name == 'darwin':
			self.gdk_target = 'quartz'
			self.sources.extend ([
				'http://github.com/jralls/gtk-osx-build/raw/master/patches/gdk-quartz-input-window.patch',
				'http://git.dronelabs.com/gtk+/patch/?id=18773097865b173fb8c28b691e23d087f0269382',
				'http://git.dronelabs.com/gtk+/patch/?id=729cbea7a2b27c4b8f2062316c0f406ab4c01dac'
			])
		elif Package.profile.name == 'linux':
			self.gdk_target = 'x11'

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (2, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

GtkPackage ()
