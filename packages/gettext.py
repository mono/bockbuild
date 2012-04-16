class GettextPackage (GnuPackage):
	def __init__ (self):
		GnuPackage.__init__ (self, 'gettext', '0.18.1.1',
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
				# Fixes building on Lion
				# http://lists.gnu.org/archive/html/bug-gnulib/2011-10/msg00018.html
				# http://git.savannah.gnu.org/gitweb/?p=gnulib.git;a=patch;h=c5728261c324a75f8d23dd7d10cb42dde9420227
				# http://git.gnome.org/browse/gtk-osx/tree/patches/gettext-bug33999-stpncpy.patch
				'patches/gettext-bug33999-stpncpy.patch',
				
				# Don't build samples
				# https://trac.macports.org/export/79183/trunk/dports/devel/gettext/files/patch-gettext-tools-Makefile.in
				'patches/gettext-no-samples.patch',
			])

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

GettextPackage ()
