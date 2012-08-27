Package ('xamarin-gtk-engine', 'master',
	sources = [ 'git@github.com:lanedo/xamarin-gtk-theme.git' ],
	override_properties = { 'configure':
		'LIBTOOL=glibtool ./autogen.sh --prefix=%{prefix}'
	}
)
