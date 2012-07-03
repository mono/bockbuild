Package ('gmp', '5.0.4', sources = [
		'ftp://ftp.gmplib.org/pub/%{name}-%{version}/%{name}-%{version}.tar.bz2'
	],
	configure_flags = ['ABI=32 --enable-cxx --disable-dependency-tracking']
)

