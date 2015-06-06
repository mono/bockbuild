class XamarinGtkThemePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'xamarin-gtk-theme', 'master',
			sources = [ 'git://github.com/mono/xamarin-gtk-theme.git' ],
			revision = '01d1c14e14c8bb8bfe7eb1e0fc043d1fff077568')

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
