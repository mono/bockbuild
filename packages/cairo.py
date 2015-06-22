class CairoPackage (CairoGraphicsXzPackage):
	def __init__ (self):
		CairoGraphicsXzPackage.__init__ (self, 'cairo', '1.12.14')
		if Package.profile.name == 'darwin':
			self.sources.extend ([
				Patch('patches/cairo-quartz-crash.patch', options = '-p1'),
				Patch('patches/cairo-fix-color-bitmap-fonts.patch', options = '-p1'),
				Patch('patches/cairo-fix-CGFontGetGlyphPath-deprecation.patch', options = '-p1'),
	#			'Patch(patches/cairo-cglayer.patch', options = '-p1'),
			])

	def build (self):
		self.configure_flags = [
			'--enable-pdf',
		]

		if Package.profile.name == 'darwin':
			self.configure_flags.extend ([
				'--enable-quartz',
				'--enable-quartz-font',
				'--enable-quartz-image',
				'--disable-xlib',
				'--without-x'
			])
		elif Package.profile.name == 'linux':
			self.configure_flags.extend ([
				'--disable-quartz',
				'--with-x'
			])

		Package.build (self)

CairoPackage ()
