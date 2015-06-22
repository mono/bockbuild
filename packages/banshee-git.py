class BansheePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'banshee', 'master')

		self.sources = [
			'git://git.gnome.org/banshee'
		]
		self.git_branch = 'master'

		self.configure = [ 'NOCONFIGURE=1 ./autogen.sh && ./profile-configure %{profile.name} --prefix=%{prefix}' ]
		self.sources.extend([
		])


BansheePackage ()
