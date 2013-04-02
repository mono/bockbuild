import os

class MonoMasterEncryptedPackage(Package):

	def __init__(self):
		Package.__init__(self, 'mono', '3.0.8',
      sources = ['git://github.com/mono/mono', 'git@github.com:xamarin/mono-extensions.git'],
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
					'patches/mcs-pkgconfig.patch'
					])

		self.configure = 'CFLAGS=-O2 ./autogen.sh'
		self.make = 'make'

	def apply_extensions(self):
		# Copied from Package#prep, makes sure we get teh latest
		# extensions
		print self.sources
		extension = self.sources[1]
		build_root = os.path.join (os.getcwd (), "..")
		dirname = os.path.join (build_root, os.path.basename (extension))
		if (os.path.exists(dirname)):
			self.cd (dirname)
			self.sh ('git clean -xfd')
			self.sh ('git reset --hard HEAD')
			self.sh ('git pull')
		else:
			self.sh ('git clone --local --shared "%s" "%s"' % (extension, dirname))

		# Use quilt to apply the patch queue
		self.cd (build_root)
		self.sh ("export QUILT_PATCHES=%s-%s-mono-extensions" % (self.name, self.version))
		self.sh ('/usr/local/bin/quilt pop -af || true') # ignore its return code
		self.sh ('/usr/local/bin/quilt push -a')

	def prep (self):
		Package.prep (self)
		self.apply_extensions()
		self.cd ('%{source_dir_name}')
		if Package.profile.name == 'darwin':
			for p in range (2, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

MonoMasterEncryptedPackage()
