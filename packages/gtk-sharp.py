def svn_co_or_up (package):
	os.chdir ('..')
	if os.path.isdir ('gtk-sharp-svn'):
		os.chdir ('gtk-sharp-svn')
		os.system ('svn up')
	else:
		os.system ('svn co http://anonsvn.mono-project.com/source/trunk/gtk-sharp gtk-sharp-svn')
		os.chdir ('gtk-sharp-svn')
	os.chdir ('..')

package = {
	'name':    'gtk-sharp',
	'version': 'svn.HEAD',
	'branch':  '212',
	'sources': [
		# 'http://ftp.novell.com/pub/mono/sources/%{name}%{branch}/%{name}-%{version}.tar.bz2'
	],
	'prep': [
		svn_co_or_up,
		'cp -a gtk-sharp-svn _build',
		'cd _build/gtk-sharp-svn'
	],
	'build': [
		'./bootstrap-for-the-insane --prefix=%{_prefix}',
		'%{__make}'
	],
	'install': [
		'%{__makeinstall}',
		'find %{_prefix}/lib/mono/gac -iregex ".*/g[td]k-sharp.dll.config" -exec sed -ie "s/x11/quartz/g" "{}" \;'
	]
}
