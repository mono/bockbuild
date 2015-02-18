Package ('xamarin-gtk-theme', 'master',
	sources = [ 'git://github.com/mono/xamarin-gtk-theme.git' ],
	override_properties = { 'configure':
		'./autogen.sh --prefix=%{prefix}'
	},
	revision = '01d1c14e14c8bb8bfe7eb1e0fc043d1fff077568',
)
