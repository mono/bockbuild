Package ('gtkimcocoa', 'master',
	sources = [ 'git://github.com/ashie/gtkimcocoa.git' ],
	override_properties = {
		'configure':
			'./autogen.sh && ./configure --prefix=%{prefix}',
		'makeinstall':
			 'make install && gtk-query-immodules-2.0 > %{prefix}/etc/gtk-2.0/gtk.immodules',
	},
	revision = 'e9f8ec81766a27ce6a6aa5231c4a5b9269a2ff99',
)
