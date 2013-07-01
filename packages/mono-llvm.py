class MonoLlvmPackage (GitHubPackage):
	def __init__ (self):
		GitHubPackage.__init__ (self, 'mono', 'llvm', '3.0',
			revision = 'f88c8bf5b31996435ed04b530cb4c7f02b244372',
			configure_flags  = ['--enable-optimized', '--enable-targets="x86 x86_64"' ]
		)

		if Package.profile.name == 'darwin' and not Package.profile.m64:
				self.configure_flags.extend ([
					'--build=i386-apple-darwin10.8.0'
				])

MonoLlvmPackage ()
