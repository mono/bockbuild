import os

class MonoLlvmPackage (GitHubPackage):
	def __init__ (self):
		GitHubPackage.__init__ (self, 'mono', 'llvm', '3.0',
			revision = 'e656caccc7dfb5c51c208906f0e176f0973f030f',
			configure_flags  = ['--enable-optimized', '--enable-assertions=no', '--enable-targets="x86 x86_64"' ]
		)

		#This package would like to be lipoed.
		if Package.profile.m64 == True:
			self.m64 = True

		#if Package.profile.name == 'darwin':
		#		self.configure_flags.extend (['CXXFLAGS=-stdlib=libc++'])

		#		os.environ ['MACOSX_DEPLOYMENT_TARGET'] = '10.8'

		self.ld_flags = [] # reset ld_flags

	def arch_build (self):

		if self.m64: #64-bit  build pass
			self.configure_flags.extend ([
				'--build=x86_64-apple-darwin11.2.0'
			])
		else:
			self.configure_flags.extend ([
				'--build=i386-apple-darwin11.2.0'
			])
		Package.arch_build (self)
		

MonoLlvmPackage ()
