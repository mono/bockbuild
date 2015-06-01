import os

class MonoMasterPackage(Package):

	def __init__(self):
		if os.getenv('MONO_VERSION') is None:
			raise Exception ('You must export MONO_VERSION to use this build profile. e.g. export MONO_VERSION=3.1.0')

		Package.__init__(self, 'mono', os.getenv('MONO_VERSION'),
			sources = [os.getenv('MONO_REPOSITORY') or 'git://github.com/mono/mono.git'],
			git_branch = os.getenv ('MONO_BRANCH') or None,
			revision = os.getenv('MONO_BUILD_REVISION'),
			configure_flags = [
				'--enable-nls=no',
				'--with-ikvm=yes'
			]
		)
		#This package would like to be lipoed.
		self.needs_lipo = True
		
		if Package.profile.name == 'darwin':
			self.configure_flags.extend([
				'--with-libgdiplus=%s/lib/libgdiplus.dylib' % Package.profile.staged_prefix,
				'--enable-loadedllvm',
				'CXXFLAGS=-stdlib=libc++'
				])

			self.sources.extend ([
					# Fixes up pkg-config usage on the Mac
					'patches/mcs-pkgconfig.patch'
					])
		else:
			self.configure_flags.extend([
				'--with-libgdiplus=%s/lib/libgdiplus.so' % Package.profile.staged_prefix
				])

		self.gcc_flags.extend (['-O2'])

		self.configure = './autogen.sh --prefix="%{package_prefix}"'

	def prep (self):
		Package.prep (self)
		for p in range (1, len (self.local_sources)):
			self.sh ('patch -p1 < "%{local_sources[' + str (p) + ']}"')

	def arch_build (self, arch):	
		if arch == 'darwin-64': #64-bit build pass
			self.local_gcc_flags = ['-m64']
			self.local_configure_flags = ['--build=x86_64-apple-darwin11.2.0']
		
		if arch == 'darwin-32': #32-bit build pass
			self.local_gcc_flags =['-m32']
			self.local_configure_flags = ['--build=i386-apple-darwin11.2.0']

	def install(self):
	        Package.install (self)
	        self.stage_file ('%{staged_prefix}/etc/mono/config')

MonoMasterPackage()
