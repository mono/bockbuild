Package ('libproxy', '0.4.4',
	sources = [
		'http://libproxy.googlecode.com/files/%{name}-%{version}.tar.gz'
	],
	override_properties = {
		'configure': './autogen.sh ; cmake '
			'[-DCMAKE_INSTALL_PREFIX=%{prefix}] '
			'[-Dlibdir=%{prefix}/lib] '
			'[-Ddatadir=%{prefix}/share] '
			'[-Dmoduledir=%{prefix}/lib/libproxy/modules] '
			'[-DPERL_VENDORINSTALL] '
			'.'
	}
)
