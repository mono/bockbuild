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
	]
}
