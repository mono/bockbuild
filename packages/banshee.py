class BansheePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'banshee', 'stable-2.4')

		self.sources = [
			'git://git.gnome.org/banshee'
		]
		self.git_branch = 'stable-2.4'

		self.configure = [ 'NOCONFIGURE=1 ./autogen.sh && ./profile-configure %{profile.name} --prefix=%{prefix}' ]
		self.sources.extend([

			# switch over from ige_* to gtk_* binding
			Patch('patches/banshee-gtk-mac-integration.patch', '-p1')
		])

	def prep (self):
		Package.prep (self)
		self.sh ('patch -p1 < %{sources[1]}')

BansheePackage ()
