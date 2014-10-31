class LibPngPackage (Package):
	def __init__ (self):
		Package.__init__(self, 'libpng', '1.4.12',
										 sources = ['http://downloads.sourceforge.net/sourceforge/libpng/libpng-1.4.12.tar.xz'],
										 configure_flags = ['--enable-shared'])

		#This package would like to be built with fat binaries
		if Package.profile.m64 == True:
			self.fat_build = True

LibPngPackage()
