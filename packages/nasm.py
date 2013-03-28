class NasmPackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'nasm', '2.10.07', sources = [
			'http://www.nasm.us/pub/nasm/releasebuilds/2.10.07/nasm-%{version}.tar.xz'
		])

NasmPackage ()
