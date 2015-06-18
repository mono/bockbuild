class GdkPixbufPackage (GnomeXzPackage):
	def __init__ (self):
		GnomeXzPackage.__init__ (self, 'gdk-pixbuf', version_major = '2.28', version_minor = '2')

		if Package.profile.name == 'darwin':
			self.sources.extend ([
				Patch('patches/gdk-pixbuf/0001-pixbuf-load-2x-variants-as-pixbuf-gobject-data.patch', options = '-p1 --ignore-whitespace'),
				Patch('patches/gdk-pixbuf/0001-pixbuf-Add-getter-setter-for-the-2x-variants.patch', options = '-p1 --ignore-whitespace'),
			])

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in self.patches:
				p.run (self)

GdkPixbufPackage ()
