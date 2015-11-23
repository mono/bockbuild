class XamarinGtkThemePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'xamarin-gtk-theme',
			sources = [ 'git://github.com/mono/xamarin-gtk-theme.git' ],
			revision = '65d4ae62093db0f0460ec83a31533670f86b592b')

	def build (self):
		try:
			self.sh ('./autogen.sh --prefix=%{staged_prefix}')
		except:
			pass
		finally:
			#self.sh ('intltoolize --force --copy --debug')
			#self.sh ('./configure --prefix="%{package_prefix}"')
			Package.build (self)


XamarinGtkThemePackage ()
