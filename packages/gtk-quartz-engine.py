Package ('gtk-quartz-engine', 'master',
	sources = [ 'git://github.com/mono/gtk-quartz-engine.git' ],
	override_properties = {
		'configure': './autogen.sh --prefix=%{prefix}'
	},
	revision = '8df9784d4572c69938f05da009bd3646e253ff9d'
)
