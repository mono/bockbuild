Package ('gtkimcocoa', '0.2',
	sources = [ 'git://github.com/ashie/gtkimcocoa.git' ],
	override_properties = {
		'configure':
			'./autogen.sh && ./configure --prefix=%{prefix}',
		'makeinstall':
			 'make install && gtk-query-immodules-2.0 > %{prefix}/etc/gtk-2.0/gtk.immodules',
	},
	revision = '66e02a793fafab876e09bb3fe5dad87365dfdb31',
)
