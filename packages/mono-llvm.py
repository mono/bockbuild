import os

class MonoLlvmPackage (GitHubPackage):
	def __init__ (self):
		GitHubPackage.__init__ (self, 'mono', 'llvm', '3.0',
			revision = '714a9d742af9ce911a3a46aa6e55041099a04be1',
			configure_flags  = ['--enable-optimized', '--enable-assertions=no', '--enable-targets="x86 x86_64"']
		)

		if Package.profile.name == 'darwin':
				self.configure_flags.extend (['CXXFLAGS=-stdlib=libc++'])

		if Package.profile.name == 'darwin' and not Package.profile.m64:
				self.configure_flags.extend ([
					'--build=i386-apple-darwin11.4.0'
				])
				os.environ ['MACOSX_DEPLOYMENT_TARGET'] = '10.8'

MonoLlvmPackage ()
