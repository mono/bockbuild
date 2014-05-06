class GettextPackage (GnuPackage):
	def __init__ (self):
		GnuPackage.__init__ (self, 'gettext', '0.18.2',
			configure_flags = [
				'--disable-java',
				'--disable-libasprintf',
				'--disable-openmp'
			]
		)

		if Package.profile.name == 'darwin':
			self.configure_flags.extend ([
				# only build the tools, osx has the lib
				# https://github.com/mxcl/homebrew/blob/master/Library/Formula/gettext.rb
				#'--without-included-gettext',
			])
			self.sources.extend ([
				# Don't build samples
				# https://trac.macports.org/export/79183/trunk/dports/devel/gettext/files/patch-gettext-tools-Makefile.in
				'patches/gettext-no-samples.patch',
			])

		#This package would like to be built with fat binaries
		if Package.profile.m64 == True:
			self.fat_build = True

	def arch_build (self, arch):
		if arch == 'darwin-fat': #multi-arch  build pass
			self.local_ld_flags = ['-arch i386' , '-arch x86_64']
			self.local_gcc_flags = ['-arch i386' , '-arch x86_64']
			self.local_configure_flags = ['--disable-dependency-tracking']

		Package.arch_build (self, arch)

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

GettextPackage ()
