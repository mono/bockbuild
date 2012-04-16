class MonoMasterPackage(Package):

	def __init__(self):
		Package.__init__(self, 'mono', '2.11',
			sources = ['git://github.com/mono/mono'],
			configure_flags = [
				'--enable-nls=no',
				'--prefix=' + Package.profile.prefix,
				'--with-ikvm=yes',
				'--with-moonlight=no'
			],
			source_dir_name = "mono-2.11.git"
		)
		if Package.profile.name == 'darwin':
			self.configure_flags.extend([
					# fix build on lion, it uses 64-bit host even with -m32
					'--build=i386-apple-darwin11.2.0',
					'--enable-loadedllvm'
					])
			self.sources.extend(['patches/pkg-config'])

		self.configure = './autogen.sh'

	def install(self):
		Package.install(self)

MonoMasterPackage()
