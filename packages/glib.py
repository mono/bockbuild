package = {
	'name':          'glib',
	'version_major': '2.22',
	'version_minor': '3',
	'version':       '%{version_major}.%{version_minor}',
	'macports_svn':  'http://svn.macports.org/repository/macports/trunk/dports/devel/glib2/files',
	'sources': [
		'http://ftp.gnome.org/pub/gnome/sources/%{name}/%{version_major}/%{name}-%{version}.tar.gz',
	]
}

if profile['name'] == 'osx':
	package['sources'].extend ([
		'%{macports_svn}/config.h.ed',
		'%{macports_svn}/patch-configure.in.diff',
		'%{macports_svn}/patch-glib-2.0.pc.in.diff',
		'%{macports_svn}/patch-gi18n.h.diff',
		'%{macports_svn}/patch-child-test.c.diff'
	])

	package['prep'] = [
		'tar xf @{sources:0}',
		'cd %{name}-%{version}'
	]

	package['prep'].extend (['patch -p0 < @{sources:%s}' % p
		for p in range (2, len (package['sources']))])

	package['build'] = [
		'autoconf',
		'%{__configure}',
		'ed - config.h < @{sources:1}',
		'%{__make}'
	]

	package['install'] = [
		'%{__makeinstall}',
		'rm %{_prefix}/lib/charset.alias'
	]
