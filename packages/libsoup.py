package = {
	'name':    'libsoup',
	'version': '2.28.2',
	'sources': [
		'http://ftp.gnome.org/pub/gnome/sources/libsoup/2.28/%{name}-%{version}.tar.bz2'
	],
	'build': [
		'%{__configure}' \
			' --without-gnome' \
			' --disable-gtk-doc' \
			' --disable-ssl',
		'%{__make}'
	]
}
