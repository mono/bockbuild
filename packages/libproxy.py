Package ('libproxy', '0.4.6',
	sources = [
		'http://libproxy.googlecode.com/files/%{name}-%{version}.tar.gz'
	],

	override_properties = {
		'configure': 'cmake '
			'-DCMAKE_INSTALL_PREFIX=%{prefix} '
			'-DBIN_INSTALL_DIR=%{prefix}/bin '
			'-DLIB_INSTALL_DIR=%{prefix}/lib '
			'-DMODULE_INSTALL_DIR=%{prefix}/lib/libproxy-%{version}/modules '
			'-DLIBEXEC_INSTALL_DIR=%{prefix}/lib/libproxy-%{version} '
			'.',

		'makeinstall': 'make install DESTDIR=%{prefix}'
	}
)
