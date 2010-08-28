class PangoPackage (GnomePackage):
	def __init__ (self):
		GnomePackage.__init__ (self,
			'pango',
			version_major = '1.28',
			version_minor = '1',
			configure_flags = [
				'--without-x'
			]
		)

		self.sources.extend ([
			# patch from bgo#321419
			'http://bugzilla-attachments.gnome.org/attachment.cgi?id=96023'
		])

	def prep (self):
		GnomePackage.prep (self)
		self.sh ('patch -p0 < "%{sources[1]}"')

PangoPackage ()
