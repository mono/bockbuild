Package ('xamarin-gtk-engine', 'master',
	sources = [ 'git@github.com:xamarin/xamarin-gtk-theme.git' ],
	override_properties = { 'configure':
		'./autogen.sh --prefix=%{prefix}'
	}
)
