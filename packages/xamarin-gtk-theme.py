Package ('xamarin-gtk-engine', 'master',
	sources = [ 'git@github.com:mono/xamarin-gtk-theme.git' ],
	override_properties = { 'configure':
		'./autogen.sh --prefix=%{prefix}'
	},
	revision = '01d77e8b0051b899837934c454d3af0d4f197b89',
)
