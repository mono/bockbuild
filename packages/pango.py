class PangoPackage (GnomeXzPackage):
	def __init__ (self):
		GnomePackage.__init__ (self,
			'pango',
			version_major = '1.30',
			version_minor = '1',
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

			# Post-1.30.1 commits from git

			# coretext: don't insert item in the hash if it originated from the hash
			'http://git.gnome.org/browse/pango/patch/?id=70a85d441d973883af4afb57599bc570eeea4c83',
		])

	def prep (self):
		GnomePackage.prep (self)
		self.sh ('patch -p0 < "%{sources[1]}"')
		if Package.profile.name == 'darwin':
			for p in range (2, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

PangoPackage ()
