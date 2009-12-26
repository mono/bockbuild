package = {
	'name':          'pango',
	'version_major': '1.26',
	'version_minor': '2',
	'version':       '%{version_major}.%{version_minor}',
	'sources': [
		'http://ftp.gnome.org/pub/gnome/sources/%{name}/%{version_major}/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure} --without-x',
		'%{__make}'
	]
}
