class PangoPackage (GnomePackage):
	def __init__ (self):
		GnomePackage.__init__ (self,
			'pango',
			version_major = '1.26',
			version_minor = '2',
			configure_flags = [
				'--without-x'
			]
		)

		self.sources.extend ([
			# patch from bgo#321419
			'http://bugzilla-attachments.gnome.org/attachment.cgi?id=96023'
		])

		if Package.profile.name == 'darwin':
			self.sources.extend ([
				'http://git.gnome.org/browse/pango/patch/?id=0f06d7758bc37a4942342d2c17a88944cbc88adb',
				# patch for bgo#608415
				'http://git.gnome.org/browse/pango/patch/?id=77f99dd9e17c5051b2b2dcfe6e7746f924e9f71b'
			])

	def prep (self):
		GnomePackage.prep (self)
		self.sh ('patch -p0 < "%{sources[1]}"')
		if Package.profile.name == 'darwin':
			self.sh ('patch -p1 < "%{sources[2]}"')
			self.sh ('patch -p1 < "%{sources[3]}"')

PangoPackage ()
