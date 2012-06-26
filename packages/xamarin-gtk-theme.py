Package ('xamarin-gtk-engine', 'master',
	sources = [ 'git://github.com/lanedo/gtk-theme-engine-osx.git' ],
	override_properties = { 'configure':
		'./autogen.sh --prefix=%{prefix}'
	}
)
