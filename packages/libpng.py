class LibPngPackage (Package):
	def __init__ (self):
		Package.__init__(self, 'libpng', '1.6.2',
			sources = ['http://downloads.sourceforge.net/sourceforge/libpng/libpng-1.6.2.tar.xz'],
			configure_flags = ['--enable-shared'])

LibPngPackage()
