GnuBz2Package ('gnutls', '2.12.20', configure_flags = [
	'--disable-guile',
	# p11 support was newly introduced in v 2.12.x
	'--without-p11-kit'
])
