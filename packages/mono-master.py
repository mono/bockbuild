import os

class MonoMasterPackage(Package):

	def __init__(self):
		Package.__init__(self, 'mono', os.getenv('MONO_VERSION'),
			sources = ['git://github.com/mono/mono.git'],
			revision = os.getenv('MONO_BUILD_REVISION'),
			configure_flags = [
				'--enable-nls=no',
				'--prefix=' + Package.profile.prefix,
				'--with-ikvm=yes',
				'--with-moonlight=no'
			]
		)
		if Package.profile.name == 'darwin':
			if not Package.profile.m64:
				self.configure_flags.extend([
					# fix build on lion, it uses 64-bit host even with -m32
					'--build=i386-apple-darwin11.2.0',
					])

			self.configure_flags.extend([
				'--enable-loadedllvm'
				])

			self.sources.extend ([
					# Fixes up pkg-config usage on the Mac
					'patches/mcs-pkgconfig.patch'
					])

		self.configure = expand_macros ('CFLAGS="%{env.CFLAGS} -O2" ./autogen.sh', Package.profile)

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

MonoMasterPackage()
