class GdkPixbufPackage (GnomeXzPackage):
	def __init__ (self):
		GnomeXzPackage.__init__ (self, 'gdk-pixbuf', version_major = '2.28', version_minor = '2')

		if Package.profile.name == 'darwin':
			self.sources.extend ([
				'patches/gdk-pixbuf/0001-pixbuf-load-2x-variants-as-pixbuf-gobject-data.patch',
				'patches/gdk-pixbuf/0001-pixbuf-Add-getter-setter-for-the-2x-variants.patch',
			])

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (1, len (self.sources)):
				self.sh ('patch -p1 --ignore-whitespace < "%{sources[' + str (p) + ']}"')

GdkPixbufPackage ()
