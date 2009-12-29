package = {
	'name':    'libxml2',
	'version': '2.7.6',
	'sources': [
		'ftp://xmlsoft.org/%{name}/%{name}-%{version}.tar.gz'			
	],
	'build': [
		'%{__configure} --with-python=no',
		'%{__make}'
	]
}
