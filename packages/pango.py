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
			# revert git 0e091322, it requires unstable glib simply for some deprecation marker macros
			'patches/pango-stable-glib.patch',

			# 3 - n
			 # [Bug 664125] - Zero-width spaces cause missing characters
			'http://git.gnome.org/browse/pango/patch/?id=dbf40154eb5804f4e8c582f12b30b8291c9c3532',
			
			# CoreText backend: implement font fallbacks
			'http://git.gnome.org/browse/pango/patch/?id=37e74619215ede8a4fa7f5edabab14b517e673b2',

			# Make CoreText backend more robust against broken fonts
			'http://git.gnome.org/browse/pango/patch/?id=38ada127bfb53911ecd64ced26fd23ec67138b43',

			# [Bug 664125] - Zero-width spaces cause missing characters
			'http://bugzilla-attachments.gnome.org/attachment.cgi?id=208003',
		])

	def prep (self):
		GnomePackage.prep (self)
		self.sh ('patch -p0 < "%{sources[1]}"')
		self.sh ('patch -p1 < "%{sources[2]}"')
		if Package.profile.name == 'darwin':
			for p in range (3, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

PangoPackage ()
