Package ('gtk-quartz-engine', 'master',
	sources = [ 'git://github.com/chkn/gtk-quartz-engine.git' ],
	override_properties = { 'configure':
		'libtoolize --force --copy && '
		'aclocal && '
		'autoheader && '
		'automake --add-missing && '
		'autoconf && '
		'./configure --prefix=%{prefix}'
	}
)
