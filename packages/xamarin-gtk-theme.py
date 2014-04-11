Package ('xamarin-gtk-theme', 'master',
	sources = [ 'git://github.com/mono/xamarin-gtk-theme.git' ],
	override_properties = { 'configure':
		'./autogen.sh --prefix=%{prefix}'
	},
	revision = 'd0d539a5d7e065e715383e665422fcef757a9753',
)
