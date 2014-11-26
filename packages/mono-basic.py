GitHubTarballPackage ('mono', 'mono-basic', '3.0', 'bd316e914e1a230c29b5d637239334df41a79c7f',
	configure = './configure --prefix="%{prefix}" --with-profile2=no',
	override_properties = { 'make': 'make' }
)
