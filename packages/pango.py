class PangoPackage (GnomeXzPackage):
	def __init__ (self):
		GnomePackage.__init__ (self,
			'pango',
			version_major = '1.35',
			version_minor = '0',
			configure_flags = [
				'--without-x'
			]
		)

		self.sources.extend ([
			# 1
			# Bug 321419 - Allow environment var substitution in Pango config
			# https://bugzilla.gnome.org/show_bug.cgi?id=321419
			'patches/pango-relative-config-file.patch',

			# BXC 10257 - Characters outside the Basic Multilingual Plane don't render correctly
			# https://bugzilla.xamarin.com/show_bug.cgi?id=10257
			'patches/pango-coretext-astral-plane-1.patch',
			'patches/pango-coretext-astral-plane-2.patch',
		])

	def prep (self):
		GnomePackage.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

PangoPackage ()
