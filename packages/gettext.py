package = {
	'name':    'gettext',
	'version': '0.17',
	'sources': [
		'http://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure} --disable-java --disable-libasprintf --disable-openmp',
		'%{__make}'
	]
}
