configure_flags = [
	'--disable-mtp',
	'--disable-daap',
	'--disable-ipod',
	'--disable-boo',
	'--disable-gnome',
	'--disable-docs',
	'--enable-osx'
]

def change_to_gitdir (*args):
	last_pwd = ''
	while not os.path.isdir ('.git'):
		os.chdir ('..')
		if last_pwd == os.getcwd ():
			break
		last_pwd = os.getcwd ()

def overwrite_launcher_script (package):
	install_bin_path = os.path.join (package['_prefix'], 'bin')
	install_lib_path = os.path.join (package['_prefix'], 'lib')

	fp = open (os.path.join (install_bin_path, 'banshee-1'), 'w')
	fp.write ('#!/usr/bin/env bash\n')
	fp.write ('export LD_LIBRARY_PATH="%s"\n' % install_lib_path)
	fp.write ('%s %s' % (os.path.join (install_bin_path, 'mono'),
		os.path.join (install_lib_path, 'banshee-1', 'Nereid.exe')))
	fp.close ()

package = {
	'name':    'banshee-1',
	'version': '1.5.2',
	'sources': [],
	'prep': [
		change_to_gitdir
	],
	'build': [
		'cp configure.ac configure.ac.orig',
		'grep -v AM_GCONF_SOURCE_2 < configure.ac.orig > configure.ac',
		'./autogen.sh --prefix=%{_prefix} ' + ' '.join (configure_flags),
		'mv configure.ac.orig configure.ac',
		'%{__make}'
	],
	'install': [
		'%{__makeinstall}',
		overwrite_launcher_script
	]
}
