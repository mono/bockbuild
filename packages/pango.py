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
			# Bug 647969 - CoreText backend needs proper font fallback/coverage support
			# https://bugzilla.gnome.org/show_bug.cgi?id=647969
			'http://bugzilla-attachments.gnome.org/attachment.cgi?id=201356',
			'http://bugzilla-attachments.gnome.org/attachment.cgi?id=203357',
			# Bug 664125 - Zero-width spaces cause missing characters
			'http://bugzilla-attachments.gnome.org/attachment.cgi?id=202190',

			# Workaround for Bug 2393 - [Gtk] Pango in Mono 2.10.7 does not work on snow leopard
			'http://bugzilla.xamarin.com/attachment.cgi?id=1053',
		])

	def prep (self):
		GnomePackage.prep (self)
		self.sh ('patch -p0 < "%{sources[1]}"')
		self.sh ('patch -p1 < "%{sources[2]}"')
		if Package.profile.name == 'darwin':
			for p in range (3, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

PangoPackage ()
