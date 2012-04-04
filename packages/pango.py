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
		])

	def prep (self):
		GnomePackage.prep (self)
		self.sh ('patch -p0 < "%{sources[1]}"')
		self.sh ('patch -p1 < "%{sources[2]}"')
#		if Package.profile.name == 'darwin':
#			for p in range (3, len (self.sources)):
#				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

PangoPackage ()
