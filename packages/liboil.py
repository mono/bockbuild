package = {
	'name':    'liboil',
	'version': '0.3.16',
	'sources': [
		'http://liboil.freedesktop.org/download/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure}' \
			' --disable-gtk-doc',
		'%{__make}'
	]
}
