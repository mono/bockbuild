package = {
	'name':    'gconf2-dummy',
	'version': '2',
	'sources': [],
	'prep':    [],
	'build':   [],
	'install': [
		'echo "AC_DEFUN([AM_GCONF_SOURCE_2],[])" > %{_prefix}/share/aclocal/gconf-2.m4'
	]
}
