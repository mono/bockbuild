configure_args = [
	'--with-gdktarget=%{gdk_target}',
	'--disable-cups',
	'--without-libjasper',
	'--without-libtiff'
]

package = {
	'name':          'gtk+',
	'version_major': '2.18',
	'version_minor': '5',
	'version':       '%{version_major}.%{version_minor}',
	'sources': [
		'http://ftp.gnome.org/pub/gnome/sources/%{name}/%{version_major}/%{name}-%{version}.tar.gz',
	],
	'prep': [
		'tar xf @{sources:0}',
		'cd %{name}-%{version}'
	],
	'build': [
		'%{__configure} ' + ' '.join (configure_args),
		'%{__make}'
	]
}

if profile['name'] == 'osx':
	package['gdk_target'] = 'quartz'
	package['sources'].extend ([
		'http://github.com/jralls/gtk-osx-build/raw/master/patches/gdk-quartz-input-window.patch'
	])
	package['prep'].append ('patch -p1 < "@{sources:1}"')
elif profile['name'] == 'linux':
	package['gdk_target'] = 'x11'
