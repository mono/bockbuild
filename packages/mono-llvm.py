import os

class MonoLlvmPackage (GitHubPackage):
	def __init__ (self):
		GitHubPackage.__init__ (self, 'mono', 'llvm', '3.0',
			revision = '0e362dce134e2234abb28465f05f0564f43b1dfb',
			configure_flags  = ['--enable-optimized', '--enable-assertions=no', '--enable-targets="x86 x86_64"' ]
		)

		#This package would like to be lipoed.
		if Package.profile.m64 == True:
			self.needs_lipo = True

		self.ld_flags = [] # TODO: find out which flags are causing issues. reset ld_flags for the package 
		self.gcc_flags = []
		self.cpp_flags = []		

	def arch_build (self, arch):	
		if arch == 'darwin-64': #64-bit  build pass
			self.local_configure_flags = ['--build=x86_64-apple-darwin11.2.0']
		
		if arch == 'darwin-32':
			self.local_configure_flags = ['--build=i386-apple-darwin11.2.0']

		#LLVM says that libstdc++4.6 is broken and we should use libstdc++4.7. This switches it to the right libstdc++.
		if Package.profile.name == 'darwin':
				self.local_configure_flags.extend (['CXXFLAGS=-stdlib=libc++'])

		Package.arch_build (self, arch, defaults = False)
		

MonoLlvmPackage ()
