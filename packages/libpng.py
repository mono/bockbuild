package = {
	'name':    'libpng',
	'version': '1.2.40',
	'sources': [
		'http://downloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure} --enable-shared',
		'%{__make}'
	]
}
