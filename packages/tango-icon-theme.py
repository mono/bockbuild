package = {
	'name':    'tango-icon-theme',
	'version': '0.8.90',
	'sources': [
		'http://tango.freedesktop.org/releases/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure} --enable-png-creation --disable-icon-framing',
		'%{__make}'
	]
}
