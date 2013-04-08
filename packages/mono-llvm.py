GitHubTarballPackage ('mono', 'llvm', '3.0', '292aa8712c3120b03f9aa1d201b2e7949adf35c3',
	configure = './configure --prefix="%{prefix}" --enable-optimized --enable-targets="x86 x86_64" --build=i386-apple-darwin10.8.0',
	override_properties = { 'make': 'make' }
)
