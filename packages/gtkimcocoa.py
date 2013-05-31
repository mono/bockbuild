Package ('gtkimcocoa', 'master',
	sources = [ 'git://github.com/ashie/gtkimcocoa.git' ],
	override_properties = {
		'configure':
			'./autogen.sh && ./configure --prefix=%{prefix}',
		'makeinstall':
			 'make install && gtk-query-immodules-2.0 > %{prefix}/etc/gtk-2.0/gtk.immodules',
	},
	revision = 'b5c4275187ac03c6a47a4fbcfd384069d0c37fad',
)
