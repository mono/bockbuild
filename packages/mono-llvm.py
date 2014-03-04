import os

class MonoLlvmPackage (GitHubPackage):
	def __init__ (self):
		GitHubPackage.__init__ (self, 'mono', 'llvm', '3.0',
			revision = 'e656caccc7dfb5c51c208906f0e176f0973f030f',
			configure_flags  = ['--enable-optimized', '--enable-assertions=no', '--enable-targets="x86 x86_64"' ]
		)

		if Package.profile.name == 'darwin' and not Package.profile.m64:
				self.configure_flags.extend ([
					'--build=i386-apple-darwin11.4.0'
				])
				os.environ ['MACOSX_DEPLOYMENT_TARGET'] = '10.8'

MonoLlvmPackage ()
