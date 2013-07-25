class GlibPackage (GnomeXzPackage):
	def __init__ (self):
		GnomeXzPackage.__init__ (self,
			'glib',
			version_major = '2.36',
			version_minor = '3')

		self.darwin = Package.profile.name == 'darwin'

		if Package.profile.name == 'darwin':
			#link to specific revisions for glib 2.30.x
			self.sources.extend ([
				# https://trac.macports.org/export/91680/trunk/dports/devel/glib2/files/config.h.ed
				'patches/glib/config.h.ed',
				# https://trac.macports.org/export/98985/trunk/dports/devel/glib2/files/patch-configure.diff
				'patches/glib/patch-configure.diff',
				# https://trac.macports.org/export/42728/trunk/dports/devel/glib2/files/patch-gi18n.h.diff
				'patches/glib/patch-gi18n.h.diff',
				# https://trac.macports.org/export/92608/trunk/dports/devel/glib2/files/patch-gio_gdbusprivate.c.diff
				'patches/glib/patch-gio_gdbusprivate.c.diff',
				# https://trac.macports.org/export/49466/trunk/dports/devel/glib2/files/patch-gio_xdgmime_xdgmime.c.diff
				'patches/glib/patch-gio_xdgmime_xdgmime.c.diff',
				# https://trac.macports.org/export/91680/trunk/dports/devel/glib2/files/patch-glib-2.0.pc.in.diff
				'patches/glib/patch-glib-2.0.pc.in.diff',
				# https://trac.macports.org/export/64476/trunk/dports/devel/glib2/files/patch-glib_gunicollate.c.diff
				'patches/glib/patch-glib_gunicollate.c.diff',

				# Bug 6156 - [gtk] Quitting the application with unsaved file and answering Cancel results in crash
				# https://bugzilla.xamarin.com/attachment.cgi?id=2214
				'patches/glib-recursive-poll.patch',
			])

	def prep (self):
		Package.prep (self)
		if self.darwin:
			for p in range (2, 8):
				self.sh ('patch -p0 < %{sources[' + str (p) + ']}')
			for p in range (8, len (self.sources)):
				self.sh ('patch --ignore-whitespace -p1 < %{sources[' + str (p) + ']}')
	
	def build (self):
		if not self.darwin:
			Package.build (self)
			return

		self.sh (
			# 'autoconf',
			'%{configure} --disable-compile-warnings',
			'ed - config.h < %{sources[1]}',
			# work around https://bugzilla.gnome.org/show_bug.cgi?id=700350
			'touch docs/reference/*/Makefile.in',
			'touch docs/reference/*/*/Makefile.in',
			'%{make}'
		)

	def install (self):
		Package.install (self)
		if self.darwin:
			# FIXME: necessary?
			self.sh ('rm -f %{prefix}/lib/charset.alias')

GlibPackage ()
