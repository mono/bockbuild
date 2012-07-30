class CairoPackage (CairoGraphicsPackage):
	def __init__ (self):
		Package.__init__ (self, 'cairo', '1.10.2')
		self.sources.extend ([
			'patches/cairo-lion.patch'
		])

	def prep (self):
		Package.prep (self)

		if Package.profile.name == 'darwin':
			for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

	def build (self):
		self.configure_flags = [
			'--enable-pdf'
		]

		if Package.profile.name == 'darwin':
			self.configure_flags.extend ([
				'--enable-quartz',
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
