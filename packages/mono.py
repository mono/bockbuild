class MonoPackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'mono', '2.8.2',
			sources = [
				'http://ftp.novell.com/pub/%{name}/sources/%{name}/%{name}-%{version}.tar.bz2',
				'patches/mono-runtime-relocation.patch'
			],
			configure_flags = [
				'--with-jit=yes',
				'--with-ikvm=no',
				'--with-mcs-docs=no',
				'--with-moonlight=no',
				'--enable-quiet-build'
			]
		)

		# Mono (in libgc) likes to fail to build randomly
		self.make = 'for((i=0;i<20;i++)); do make && break; done'

#	def prep (self):
#		Package.prep (self)
#		self.sh ('patch -p1 < "%{sources[1]}"')

	def install (self):
		Package.install (self)
		if Package.profile.name == 'darwin':
			self.sh ('sed -ie "s/libcairo.so.2/libcairo.2.dylib/" "%{prefix}/etc/mono/config"')

MonoPackage ()
