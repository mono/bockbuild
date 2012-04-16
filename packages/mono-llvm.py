GitHubTarballPackage ('mono', 'llvm', '2.11', '41765e2a354ca7aa88ddb1b8d6b5eb7527556b51',
	configure = './configure --prefix="%{prefix}" --enable-optimized --enable-targets="x86 x86_64" --target=i386-apple-darwin10.8.0',
	override_properties = { 'make': 'make' }
)
