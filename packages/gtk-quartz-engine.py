Package ('gtk-quartz-engine', 'master',
	sources = [ 'git://github.com/mono/gtk-quartz-engine.git' ],
	override_properties = {
		'configure': './autogen.sh --prefix=%{package_prefix}',
		'needs_lipo' : True
	},
	revision = '8e0437c006eae316389fa89a670de6a7b56e9136'
)
