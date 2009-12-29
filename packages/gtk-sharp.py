def svn_co_or_up (package):
	os.chdir ('..')
	if os.path.isdir ('svn'):
		os.chdir ('svn')
		os.system ('svn up')
	else:
		os.system ('svn co http://anonsvn.mono-project.com/source/branches/gtk-sharp-2-12-branch svn')
		os.chdir ('svn')
	os.chdir ('..')

package = {
	'name':    'gtk-sharp',
	'version': '2.12.10-svn',
	'branch':  '212',
	'sources': [
		# 'http://ftp.novell.com/pub/mono/sources/%{name}%{branch}/%{name}-%{version}.tar.bz2'
	],
	'prep': [
		svn_co_or_up,
		'cp -a svn _build',
		'cd _build/svn'
	],
	'build': [
		'./bootstrap-2.12 --prefix=%{_prefix}',
		'%{__make}'
	]
}
