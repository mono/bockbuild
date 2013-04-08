class NantPackage (Package):
	def __init__(self):
		Package.__init__(self, 'nant', '0.91', sources = ['http://sourceforge.net/projects/nant/files/nant/0.91/nant-0.91-src.tar.gz'])

	def build(self):
		self.sh ('make install prefix="%{prefix}"')

NantPackage ()
