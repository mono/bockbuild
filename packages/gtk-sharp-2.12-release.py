class GtkSharp212ReleasePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'gtk-sharp', '2.12.12', sources = ['http://files.xamarin.com/~alan/gtk-sharp-2.12.12.tar.gz'])
		# self.configure = './bootstrap-2.12 --prefix="%{prefix}"'
		self.make = 'make CSC=gmcs'

GtkSharp212ReleasePackage ()
