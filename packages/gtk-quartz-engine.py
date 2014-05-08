class GtkQuartzEnginePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'gtk-quartz-engine', 'master',
			sources = [ 'git://github.com/mono/gtk-quartz-engine.git' ],
			override_properties = {
				'configure': './autogen.sh --prefix=%{package_prefix}',
				'needs_lipo' : True
			},
			revision = '8e0437c006eae316389fa89a670de6a7b56e9136')

	def arch_build (self, arch):	
		if arch == 'darwin-64': #64-bit  build pass
			self.local_configure_flags = ['--build=x86_64-apple-darwin11.2.0']
			self.local_gcc_flags = ['-m64']
			self.local_ld_flags = ['-m64']
		
		if arch == 'darwin-32':
			self.local_configure_flags = ['--build=i386-apple-darwin11.2.0']
			self.local_gcc_flags = ['-m32']
			self.local_ld_flags = ['-m32']

		Package.arch_build (self, arch)

GtkQuartzEnginePackage ()
