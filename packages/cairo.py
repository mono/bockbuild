configure_args = [
	'--enable-pdf'
]

if profile['name'] == 'osx':
	configure_args.extend ([
		'--enable-quartz',
		'--disable-xlib=no',
		'--without-x'
	])
elif profile['name'] == 'linux':
	configure_args.extend ([
		'--disable-quartz',
		'--with-x'
	])

package = {
	'name':    'cairo',
	'version': '1.8.8',
	'sources': [
		'http://cairographics.org/releases/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure} ' + ' '.join (configure_args),
		'%{__make}'
	]
}
