class XamarinGtkThemePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'xamarin-gtk-theme',
			sources = [ 'git://github.com/mono/xamarin-gtk-theme.git' ],
			revision = 'e7d5c22ae63811dba9b681b0c7a030424e8429a6')

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
