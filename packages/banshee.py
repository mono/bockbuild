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
	'sources': [
		'http://download.banshee-project.org/banshee/stable/%{version}/%{name}-%{version}.tar.bz2'
	],
	'build': [
		'%{__configure} ' + ' '.join (configure_flags),
		'%{__make}'
	]
}
