package = {
	'name':    'fontconfig',
	'version': '2.7.3',
	'sources': [
		'http://www.fontconfig.org/release/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure} --disable-docs',
		'%{__make}'
	]
}
