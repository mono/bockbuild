class LibTiffPackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'tiff', '4.0.3',
			configure_flags = [
			],
			sources = [
				'http://download.osgeo.org/libtiff/tiff-%{version}.tar.gz',
			])

		if Package.profile.name == 'darwin':
			self.sources.extend ([
				# Fix Snow Leopard build
				# http://jira.freeswitch.org/secure/attachment/17487/tiff-4.0.2-macosx-2.patch
				Patch('patches/tiff-4.0.2-macosx-2.patch', '-p1'),
			])

LibTiffPackage ()
