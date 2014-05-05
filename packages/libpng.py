class LibPngPackage (Package):
	def __init__ (self):
		Package.__init__(self, 'libpng', '1.4.12',
										 sources = ['http://downloads.sourceforge.net/sourceforge/libpng/libpng-1.4.12.tar.xz'],
										 configure_flags = ['--enable-shared'])

		#This package would like to be built with fat binaries
		if Package.profile.m64 == True:
			self.fat_build = True

	def arch_build (self, arch):
		if arch == 'darwin-fat': #multi-arch  build pass
			self.local_ld_flags = ['-arch i386' , '-arch x86_64']
			self.local_gcc_flags = ['-arch i386' , '-arch x86_64', '-Os']
			self.local_configure_flags = ['--disable-dependency-tracking']

		Package.arch_build (self, arch)


LibPngPackage()
