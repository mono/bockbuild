class MonoLlvmPackage (GitHubPackage):
	def __init__ (self):
		GitHubPackage.__init__ (self, 'mono', 'llvm', '3.0',
			revision = '8bdedb58a7a8d801c5b229b67f3de48e421928a1',
			configure_flags  = ['--enable-optimized', '--enable-targets="x86 x86_64"' ]
		)

		if Package.profile.name == 'darwin' and not Package.profile.m64:
				self.configure_flags.extend ([
					'--build=i386-apple-darwin10.8.0'
				])

MonoLlvmPackage ()
