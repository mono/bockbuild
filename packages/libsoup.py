package = {
	'name':         'libsoup',
	'version_major': '2.28',
	'version_minor': '2',
	'version':       '%{version_major}.%{version_minor}',
	'sources': [
		'http://ftp.gnome.org/pub/gnome/sources/libsoup/%{version_major}/%{name}-%{version}.tar.bz2'
	],
	'build': [
		'%{__configure}' \
			' --without-gnome' \
			' --disable-gtk-doc' \
			' --disable-ssl',
		'%{__make}'
	]
}
