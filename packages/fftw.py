Package ('fftw', '3.3.2',
	sources = [ 'http://www.fftw.org/%{name}-%{version}.tar.gz'],

	# banshee's lastfmfingerprint addin requires
	# the single-precision variant
	configure_flags = [
		'--enable-single',
		'--enable-shared'
	]
)
