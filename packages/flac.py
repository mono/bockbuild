package = {
	'name':    'flac',
	'version': '1.2.1',
	'sources': [
		'http://downloads.xiph.org/releases/%{name}/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure}' \
			' --disable-asm-optimizations' \
			' --disable-cpplibs',
		'%{__make}'
	]
}
