Package ('gtk-quartz-engine', 'master',
	sources = [ 'git://github.com/mono/gtk-quartz-engine.git' ],
	override_properties = {
		'configure': './autogen.sh --prefix=%{prefix}'
	},
	revision = '2bc5380f27d5b41d54bd91638f6443f0bc2dda69'
)
