package = {
	'name':    'cairo',
	'version': '1.8.8',
	'sources': [
		'http://cairographics.org/releases/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure} --enable-pdf --enable-quartz --enable-xlib=no --without-x',
		'%{__make}'
	]
}
