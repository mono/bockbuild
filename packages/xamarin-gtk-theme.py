Package ('xamarin-gtk-theme', 'master',
	sources = [ 'git://github.com/mono/xamarin-gtk-theme.git' ],
	override_properties = { 'configure':
		'./autogen.sh --prefix=%{prefix}'
	},
	revision = '8840eb554ce193d8660aeb3ae4957f49904edaae',
)
