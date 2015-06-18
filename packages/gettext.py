class GettextPackage (GnuPackage):
	def __init__ (self):
		GnuPackage.__init__ (self, 'gettext', '0.18.2',
			configure_flags = [
				'--disable-java',
				'--disable-libasprintf',
				'--disable-openmp',
				'--with-included-glib'
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
				Patch('patches/gettext-no-samples.patch', options = '-p1'),
			])

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in self.patches:
				p.run (self)

GettextPackage ()
