class PangoPackage (GnomePackage):
	def __init__ (self):
		GnomePackage.__init__ (self,
			'pango',
			version_major = '1.29',
			version_minor = '5',
			configure_flags = [
				'--without-x'
			]
		)

		self.sources.extend ([
			# 1
			# Bug 321419 - Allow environment var substitution in Pango config
			# https://bugzilla.gnome.org/show_bug.cgi?id=321419
			'http://bugzilla-attachments.gnome.org/attachment.cgi?id=96023',
			
			# 2
			# revert this, it requires unstable glib simply for some deprecation marker macros
			'http://git.gnome.org/browse/pango/patch/?id=0e091322',
			
			# 3 - n

			'patches/pango-stable-glib.patch',

			# Bug 647969 - CoreText backend needs proper font fallback/coverage support
			# https://bugzilla.gnome.org/show_bug.cgi?id=647969
			'http://bugzilla-attachments.gnome.org/attachment.cgi?id=201356',
			'http://bugzilla-attachments.gnome.org/attachment.cgi?id=203357',
			# Bug 664125 - Zero-width spaces cause missing characters
			'http://bugzilla-attachments.gnome.org/attachment.cgi?id=202190',
		])

	def prep (self):
		GnomePackage.prep (self)
		self.sh ('patch -p0 < "%{sources[1]}"')
		self.sh ('patch -p1 -R < "%{sources[2]}"')
		if Package.profile.name == 'darwin':
			for p in range (3, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

PangoPackage ()
