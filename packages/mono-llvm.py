import os

class MonoLlvmPackage (GitHubPackage):
	def __init__ (self):
		GitHubPackage.__init__ (self, 'mono', 'llvm', '3.0',
			revision = 'e656caccc7dfb5c51c208906f0e176f0973f030f',
			configure_flags  = ['--enable-optimized', '--enable-assertions=no', '--enable-targets="x86 x86_64"' ]
		)

		#This package would like to be lipoed.
		if Package.profile.m64 == True:
			self.needs_lipo = True

		#if Package.profile.name == 'darwin':
		#		self.configure_flags.extend (['CXXFLAGS=-stdlib=libc++'])

		#		os.environ ['MACOSX_DEPLOYMENT_TARGET'] = '10.8'

		self.ld_flags = [] # TODO: find out which flags are causing issues. reset ld_flags for the package 
		self.gcc_flags = []
		self.cpp_flags = []		

	def arch_build (self, arch):	
		if arch == 'darwin-64': #64-bit  build pass
			self.local_configure_flags = ['--build=x86_64-apple-darwin11.2.0']
		
		if arch == 'darwin-32':
			self.local_configure_flags = ['--build=i386-apple-darwin11.2.0']

		Package.arch_build (self, arch)
		

MonoLlvmPackage ()
