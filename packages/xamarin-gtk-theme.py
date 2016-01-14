class XamarinGtkThemePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'xamarin-gtk-theme',
			sources = [ 'git://github.com/mono/xamarin-gtk-theme.git' ],
			revision = '7749193e84e68697e81dd069cb6be712ff3dbff1')

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
