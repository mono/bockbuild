class GtkSharpPackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'gtk-sharp', '2-12-branch')
		self.commit = 'febd3819c52a51d247c67d156ee3fe68d730bc54'
		self.source_dir_name = 'mono-gtk-sharp-%s' % self.commit[:7]
		self.configure = './bootstrap-2.12 --prefix="%{prefix}"'
		self.sources = [
			'http://github.com/mono/gtk-sharp/tarball/%{commit}',
		]

	def prep (self):
		Package.prep (self)
		for p in range (1, len (self.sources)):
			self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

GtkSharpPackage ()
