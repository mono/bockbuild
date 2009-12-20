configure_flags = [
	'--disable-cpplibs'
]

if profile['name'] == 'osx':
	configure_flags.append ('--disable-asm-optimizations')

package = {
	'name':    'flac',
	'version': '1.2.1',
	'sources': [
		'http://downloads.xiph.org/releases/%{name}/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure}' + ' '.join (configure_flags),
		'%{__make}'
	]
}
