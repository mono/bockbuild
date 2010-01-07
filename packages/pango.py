GnomePackage ('pango',
	version_major = '1.26',
	version_minor = '2',
	configure_flags = [
		'--without-x',
		'--with-included-modules=basic-atsui'
	],
	override_properties = {
		'make':
			'( make -j%s -k -C modules || true ); '
			'make -j%s' % \
				(Package.profile.cpu_count, Package.profile.cpu_count)
	}
)
