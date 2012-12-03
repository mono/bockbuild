class GtkSharpPackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'gtk-sharp', '2-12-branch')
		self.commit = 'acbb04600d2dbdbe889117c07ee660818abd7070'
		self.source_dir_name = 'mono-gtk-sharp-%s' % self.commit[:7]
		self.configure = './bootstrap-2.12 --prefix="%{prefix}"'
		self.sources = [
			'http://github.com/mono/gtk-sharp/tarball/%{commit}'
		]

GtkSharpPackage ()
