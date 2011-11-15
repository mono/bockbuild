class PangoPackage (GnomePackage):
	def __init__ (self):
		GnomePackage.__init__ (self,
			'pango',
			version_major = '1.29',
			version_minor = '4',
			configure_flags = [
				'--without-x'
			]
		)

		self.sources.extend ([
			# patch from bgo#321419
			'http://bugzilla-attachments.gnome.org/attachment.cgi?id=96023',
			# CoreText: stricter handling of FontSymbolic traits
			'http://git.gnome.org/browse/pango/patch/?id=cce4c9f84350bb53371323ab96ccf9245e014f75',
			# Get _pango_get_lc_ctype from system prefs on Mac OS X
			'http://git.gnome.org/browse/pango/patch/?id=c21b1bfe1278de08673c495ba398fbdee874a778',
			# Bug 647969 - CoreText backend needs proper font fallback/coverage support
			# https://bugzilla.gnome.org/show_bug.cgi?id=647969
			'http://bugzilla-attachments.gnome.org/attachment.cgi?id=201356',
		])

	def prep (self):
		GnomePackage.prep (self)
		self.sh ('patch -p0 < "%{sources[1]}"')
		if Package.profile.name == 'darwin':
			for p in range (2, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

PangoPackage ()
