Package ('gtkimcocoa', 'master',
	sources = [ 'git://github.com/mhutch/gtkimcocoa.git' ],
	override_properties = {
		'configure':
			'./autogen.sh && ./configure --prefix=%{prefix}',
		'makeinstall':
			 'make install && gtk-query-immodules-2.0 > %{prefix}/etc/gtk-2.0/gtk.immodules',
	},
	revision = '663108828f8d1199a190b696815be80ff3e4b2ae',
)
