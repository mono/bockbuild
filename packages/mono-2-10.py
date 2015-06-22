import os

class MonoTwoTenPackage(Package):

	def __init__(self):
		Package.__init__(self, 'mono', '2.10.12',
			sources = ['git://github.com/mono/mono.git'],
			git_branch = 'mono-2-10',
			revision = os.getenv('MONO_BUILD_REVISION'),
			configure_flags = [
				'--enable-nls=no',
				'--prefix=' + Package.profile.prefix,
				'--with-ikvm=yes',
				'--with-moonlight=no'
			]
		)
		if Package.profile.name == 'darwin':
			self.configure_flags.extend([
					# fix build on lion, it uses 64-bit host even with -m32
					'--build=i386-apple-darwin11.2.0',
					'--enable-loadedllvm'
					])

			self.sources.extend ([
					# Fixes up pkg-config usage on the Mac
					Patch('patches/mcs-pkgconfig.patch', '-p1')
					])

		self.configure = './autogen.sh'

MonoTwoTenPackage()
