Package ('liboil', '0.3.16',
	sources = [
		'http://%{name}.freedesktop.org/download/%{name}-%{version}.tar.gz'
	],
	configure_flags = [
		'--disable-gtk-doc'
	]
)
