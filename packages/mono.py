configure_flags = [
	'--with-jit=yes',
	'--with-ikvm=no',
	'--with-mcs-docs=no',
	'--with-moonlight=no',
	'--enable-quiet-build'
]

package = {
	'name':    'mono',
	'version': '2.6.1',
	'sources': [
		'http://ftp.novell.com/pub/%{name}/sources/%{name}/%{name}-%{version}.tar.bz2'
	],
	'build': [
		'%{__configure} ' + ' '.join (configure_flags),
		'%{__make}'
	],
	'install': [
		'%{__makeinstall}'
	]
}

if profile['name'] == 'osx':
	package['install'].extend ([
		'sed -ie "s/libcairo.so.2/libcairo.2.dylib/" "%{_prefix}/etc/mono/config"'
	])
