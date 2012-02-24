class GtkPackage (GnomeXzPackage):
	def __init__ (self):
		GnomeXzPackage.__init__ (self, 'gtk+',
			version_major = '2.24',
			version_minor = '10',
			configure_flags = [
				'--with-gdktarget=%{gdk_target}',
#				'--disable-cups',
			]
		)

		self.gdk_target = 'x11'
		if Package.profile.name == 'darwin':
			self.gdk_target = 'quartz'
			self.sources.extend ([
				# smooth scrolling, https://bugzilla.gnome.org/show_bug.cgi?id=516725
				'http://bugzilla-attachments.gnome.org/attachment.cgi?id=201916',

				# make new modifier behviour opt-in, so as not to break old versions of MonoDevelop
				'patches/gdk-quartz-set-fix-modifiers-hack-v3.patch',

				# window resizing, https://bugzilla.xamarin.com/show_bug.cgi?id=3120
				'https://bugzilla.xamarin.com/attachment.cgi?id=1386',
				'https://bugzilla.xamarin.com/attachment.cgi?id=1387',

				# https://bugzilla.xamarin.com/show_bug.cgi?id=3505
				'patches/gtk-mac-function-keys.patch',

				# attempt to work around 2158 - [GTK] crash triggering context menu
				# also prints some warnings that may help to debug the real issue
				'patches/gtk-bxc-2158-debugging.patch',
			])

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

GtkPackage ()
