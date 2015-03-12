GitHubTarballPackage ('mono', 'mono-basic', '3.0', 'f8df8d804a4ce267f98161678aeaf5e20d6558b9',
	configure = './configure --prefix="%{staged_prefix}"',
	override_properties = { 'make': 'make',
				'makeinstall' : 'make install' }
)
