class GtkSharp212ReleasePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'gtk-sharp', '2.12.11')
		# self.configure = './bootstrap-2.12 --prefix="%{prefix}"'
		self.sources = ['http://download.mono-project.com/sources/gtk-sharp212/gtk-sharp-2.12.11.tar.bz2']
		self.make = 'make CSC=gmcs'

GtkSharp212ReleasePackage ()
