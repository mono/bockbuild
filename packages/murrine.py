class MurrinePackage (GnomePackage):
	def __init__ (self):
		GnomePackage.__init__ (self,
			'murrine',
			version_major = '0.98',
			version_minor = '1')

		self.configure = 'autoreconf -fi && ./configure --prefix="%{prefix}"'

		self.sources.append ('patches/murrine-link-pixman.patch')
		# FIXME: this may need porting
		# self.sources.append ('patches/murrine-osx.patch')

	def prep (self):
		Package.prep (self)
		self.sh ('patch -p1 < "%{sources[1]}"')

MurrinePackage ()
