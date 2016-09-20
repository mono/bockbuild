class GtkSharp212ReleasePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'gtk-sharp',
			sources = ['git://github.com/mono/gtk-sharp.git'],
			git_branch = 'gtk-sharp-2-12-branch',
			revision = '037d80632c7b2c87377a7a80463537685886ee85',
			override_properties = {
				'configure': './bootstrap-2.12 --prefix=%{package_prefix}',
			}
		)
		self.make = 'make CSC=mcs'

GtkSharp212ReleasePackage ()
