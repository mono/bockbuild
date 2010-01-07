class GlibPackage (GnomePackage):
	def __init__ (self):
		GnomePackage.__init__ (self,
			'glib',
			version_major = '2.22',
			version_minor = '3')

		self.darwin = Package.profile.name == 'darwin'
		self.macports_svn = 'http://svn.macports.org/repository/macports/trunk/dports/devel/glib2/files'

		if Package.profile.name == 'darwin':
			self.sources.extend (['%{macports_svn}/' + s for s in [
				'config.h.ed',
				'patch-configure.in.diff',
				'patch-glib-2.0.pc.in.diff',
				'patch-gi18n.h.diff',
				'patch-child-test.c.diff'
			]])

	def prep (self):
		Package.prep (self)
		if self.darwin:
			for p in range (2, len (self.sources)):
				self.sh ('patch -p0 < %{sources[' + str (p) + ']}')
	
	def build (self):
		if not self.darwin:
			Package.build (self)
			return

		self.sh (
			'autoconf',
			'%{configure}',
			'ed - config.h < %{sources[1]}',
			'%{make}'
		)

	def install (self):
		Package.install (self)
		if self.darwin:
			# FIXME: necessary?
			self.sh ('rm %{prefix}/lib/charset.alias')

GlibPackage ()
