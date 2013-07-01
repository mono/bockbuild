class MonoPackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'mono', '2.10.9',
			sources = [
				'http://download.mono-project.com/sources/%{name}/%{name}-%{version}.tar.bz2',
				'patches/mono-gtk-sharp-profiler.patch',
				'patches/xbuild-bug4365.patch'
			],
			configure_flags = [
				'--with-jit=yes',
				'--with-ikvm=no',
				'--with-mcs-docs=no',
				'--with-moonlight=no',
				'--enable-quiet-build',
			]
		)
		if Package.profile.name == 'darwin' and not Package.profile.m64:
			self.configure_flags.extend ([
				# fix build on lion, it uses 64-bit host even with -m32
				'--build=i386-apple-darwin11.2.0',
			])

		# Mono (in libgc) likes to fail to build randomly
		self.make = 'for i in 1 2 3 4 5 6 7 8 9 10; do make && break; done'

	def prep (self):
		Package.prep (self)
		self.sh ('patch -p1 < "%{sources[2]}"')

	def install (self):
		Package.install (self)
		if Package.profile.name == 'darwin':
			self.sh ('sed -ie "s/libcairo.so.2/libcairo.2.dylib/" "%{prefix}/etc/mono/config"')

MonoPackage ()
