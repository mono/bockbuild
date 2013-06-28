Package ('xamarin-gtk-theme', 'master',
	sources = [ 'git://github.com/mono/xamarin-gtk-theme.git' ],
	override_properties = { 'configure':
		'./autogen.sh --prefix=%{prefix}'
	},
	revision = '9887890ccbcfb1ed6812533d09312f0e1fd8f1a4',
)
