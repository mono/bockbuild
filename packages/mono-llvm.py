class MonoLlvmPackage (GitHubPackage):
	def __init__ (self):
		GitHubPackage.__init__ (self, 'mono', 'llvm', '3.0',
			revision = '7e2ee51f8cad6ddeebdc66d8288cb21685422d42',
			configure_flags  = ['--enable-optimized', '--enable-targets="x86 x86_64"' ]
		)

		if Package.profile.name == 'darwin' and not Package.profile.m64:
				self.configure_flags.extend ([
					'--build=i386-apple-darwin10.8.0'
				])

MonoLlvmPackage ()
