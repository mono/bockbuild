import os

class MonoLlvmPackage (GitHubPackage):
	def __init__ (self):
		GitHubPackage.__init__ (self, 'mono', 'llvm', '3.0',
			revision = '74259cd683e9799b0e5ec9cb25a041c1ec0eb3d1',
			configure_flags  = ['--enable-optimized', '--enable-assertions=no', '--enable-targets="x86 x86_64"' ]
		)

		#if Package.profile.name == 'darwin':
		#		self.configure_flags.extend (['CXXFLAGS=-stdlib=libc++'])

		if Package.profile.name == 'darwin' and not Package.profile.m64:
				self.configure_flags.extend ([
					'--build=i386-apple-darwin11.4.0'
				])
				os.environ ['MACOSX_DEPLOYMENT_TARGET'] = '10.8'

MonoLlvmPackage ()
