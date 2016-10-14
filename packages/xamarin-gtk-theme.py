class XamarinGtkThemePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'xamarin-gtk-theme',
			sources = [ 'git://github.com/mono/xamarin-gtk-theme.git' ],
			revision = 'b22bd9d635c7092f3eee8823ed9aea56be5f51f3')

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
