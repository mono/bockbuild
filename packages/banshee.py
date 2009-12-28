configure_flags = [
	'--disable-mtp',
	'--disable-daap',
	'--disable-ipod',
	'--disable-boo',
	'--disable-gnome',
	'--disable-docs'
]

package = {
	'name':    'banshee-1',
	'version': '1.5.2',
	'sources': [],
	'prep': [
		'cd ../../../../..',
		'pwd'
	],
	'build': [
		'cp configure.ac configure.ac.orig',
		'grep -v AM_GCONF_SOURCE_2 < configure.ac.orig > configure.ac',
		'./autogen.sh --prefix=%{_prefix} ' + ' '.join (configure_flags),
		'%{__make}'
	],
	'install': []
}
