GitHubTarballPackage ('mono', 'llvm', '2.10', '943edbc1a93df204d687d82d34d2b2bdf9978f4e',
	configure = './configure --prefix="%{prefix}" --enable-optimized --enable-targets="x86 x86_64" --target=i386-apple-darwin10.8.0',
	override_properties = { 'make': 'make' }
)
