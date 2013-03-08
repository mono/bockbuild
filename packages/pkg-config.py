class PkgConfigPackage (Package):
	def __init__ (self):
		Package.__init__(self,
										 name = 'pkg-config',
										 version = '0.25',
										 sources = ['http://storage.bos.xamarin.com/bockbuild-sources/pkg-config-0.25.tar.gz'])

PkgConfigPackage ()



