Package ('xamarin-gtk-theme', 'master',
	sources = [ 'git://github.com/mono/xamarin-gtk-theme.git' ],
	override_properties = { 'configure':
		'./autogen.sh --prefix=%{prefix}'
	},
	revision = '3ccf8317b6b1503c584584064e39f4643fb90069',
)
