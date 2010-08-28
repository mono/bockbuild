class GtkSharpPackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'gtk-sharp', '2-12-branch')
		self.commit = 'b078aacaf263af84605812d778b62afbdf3e1b59'
		self.source_dir_name = 'mono-gtk-sharp-%s' % self.commit[:7]
		self.configure = './bootstrap-2.12 --prefix="%{prefix}"'
		self.sources = [
			'http://github.com/mono/gtk-sharp/tarball/%{commit}'
		]

GtkSharpPackage ()
