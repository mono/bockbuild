class LibPngPackage (Package):
	def __init__ (self):
		Package.__init__(self, 'libpng', '1.4.4', 
										 sources = ['http://downloads.sourceforge.net/sourceforge/libpng/libpng-1.4.4.tar.gz'],
										 configure_flags = ['--enable-shared'])

LibPngPackage()
