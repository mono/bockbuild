configure_flags = [
	'--disable-mtp',
	'--disable-daap',
	'--disable-ipod',
	'--disable-boo',
	'--disable-gnome',
	'--disable-docs'
]

if profile['name'] == 'osx':
	configure_flags.append ('--enable-osx')

def change_to_gitdir (*args):
	last_pwd = ''
	while not os.path.isdir ('.git'):
		os.chdir ('..')
		if last_pwd == os.getcwd ():
			break
		last_pwd = os.getcwd ()

package = {
	'name':    'banshee-1',
	'version': '1.5.2',
	'sources': [],
	'prep': [
		change_to_gitdir
	],
	'build': [
		'./autogen.sh --prefix=%{_prefix} ' + ' '.join (configure_flags),
		'%{__make}'
	]
}
