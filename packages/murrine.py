class MurrinePackage (GnomePackage):
	def __init__ (self):
		GnomePackage.__init__ (self,
			'murrine',
			version_major = '0.90',
			version_minor = '3')

		self.sources.append ('patches/murrine-osx.patch')

	def prep (self):
		Package.prep (self)
		self.sh ('patch -p1 < "%{sources[1]}"')

MurrinePackage ()
