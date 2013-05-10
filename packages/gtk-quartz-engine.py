Package ('gtk-quartz-engine', 'master',
	sources = [ 'git://github.com/mono/gtk-quartz-engine.git' ],
	override_properties = {
		'configure': './autogen.sh --prefix=%{prefix}'
	},
	revision = '391a54a1462b67097424e0170d168f95e596dea8'
)
