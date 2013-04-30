class GtkSharp212ReleasePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'gtk-sharp', '2.12.21', sources = ['http://download.mono-project.com/sources/gtk-sharp212/gtk-sharp-2.12.21.tar.gz'])
		# self.configure = './bootstrap-2.12 --prefix="%{prefix}"'
		self.make = 'make CSC=gmcs'

GtkSharp212ReleasePackage ()
