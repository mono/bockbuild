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
				'http://github.com/jralls/gtk-osx-build/raw/master/patches/gdk-quartz-input-window.patch'
			])
		elif Package.profile.name == 'linux':
			self.gdk_target = 'x11'

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			self.sh ('patch -p1 < "%{sources[1]}"')

GtkPackage ()
