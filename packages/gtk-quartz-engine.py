Package ('gtk-quartz-engine', 'master',
	sources = [ 'git://github.com/chkn/gtk-quartz-engine.git' ],
	override_properties = {
		'configure': './autogen.sh --prefix=%{prefix}'
	}
)
