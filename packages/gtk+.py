package = {
	'name':          'gtk+',
	'version_major': '2.18',
	'version_minor': '5',
	'version':       '%{version_major}.%{version_minor}',
	'sources': [
		'http://ftp.gnome.org/pub/gnome/sources/%{name}/%{version_major}/%{name}-%{version}.tar.gz',
		'http://github.com/jralls/gtk-osx-build/raw/master/patches/gdk-quartz-input-window.patch'
	],
	'prep': [
		'tar xf @{sources:0}',
		'cd %{name}-%{version}',
		'patch -p1 < @{sources:1}'
	],
	'build': [
		'%{__configure} --with-gdktarget=quartz --without-libjasper --without-libtiff',
		'%{__make}'
	]
}
