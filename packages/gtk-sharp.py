class GtkSharp212ReleasePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'gtk-sharp',
			sources = ['git://github.com/mono/gtk-sharp.git'],
			git_branch = 'gtk-sharp-2-12-branch',
			revision = '6454e78e07f65cb3544414dbd654d5e9c5b64bd0',
			override_properties = {
				'configure': './bootstrap-2.12 --prefix=%{package_prefix}',
			}
		)
		self.make = 'make CSC=mcs'

GtkSharp212ReleasePackage ()
