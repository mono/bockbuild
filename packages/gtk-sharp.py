class GtkSharp212ReleasePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'gtk-sharp',
			sources = ['git://github.com/mono/gtk-sharp.git'],
			git_branch = 'gtk-sharp-2-12-branch',
			revision = '9dfddcdc2ee7ff4aa062926b9950b9c91fe130dc',
			override_properties = {
				'configure': './bootstrap-2.12 --prefix=%{package_prefix}',
			}
		)
		self.make = 'make CSC=mcs'

GtkSharp212ReleasePackage ()
