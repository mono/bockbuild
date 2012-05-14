class PangoPackage (GnomeXzPackage):
	def __init__ (self):
		GnomePackage.__init__ (self,
			'pango',
			version_major = '1.30',
			version_minor = '0',
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

			# Post-1.30.0 commits from git

			# Use same font family name fallback in pango_core_text_font_map_init
			'http://git.gnome.org/browse/pango/patch/?id=216d03ba5023b247515e2adf5df658c0e4e90b3d',
		])

	def prep (self):
		GnomePackage.prep (self)
		self.sh ('patch -p0 < "%{sources[1]}"')
		if Package.profile.name == 'darwin':
			for p in range (2, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

PangoPackage ()
