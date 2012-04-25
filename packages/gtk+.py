class GtkPackage (GnomeXzPackage):
	def __init__ (self):
		GnomeXzPackage.__init__ (self, 'gtk+',
			version_major = '2.24',
			version_minor = '10',
			configure_flags = [
				'--with-gdktarget=%{gdk_target}',
				'--prefix="%{prefix}"'
#				'--disable-cups',
			]
		)
		self.configure = './configure'
		self.gdk_target = 'x11'

		if Package.profile.name == 'darwin':
			self.gdk_target = 'quartz'
			self.sources.extend ([
				# smooth scrolling, https://bugzilla.gnome.org/show_bug.cgi?id=516725
				'http://bugzilla-attachments.gnome.org/attachment.cgi?id=201916',

				# make new modifier behviour opt-in, so as not to break old versions of MonoDevelop
				'patches/gdk-quartz-set-fix-modifiers-hack-v3.patch',

				# post-2.24.10 commits
				# quartz: make function keys work (again?)
				'http://git.gnome.org/browse/gtk+/patch/?id=0b24f16241f563b71c0c827bbb760a72df892b6a',
				# quartz: remove excess initializers in the new modifier_keys array
				'http://git.gnome.org/browse/gtk+/patch/?id=dca75f3b938d3744ec493466d26e0cfb024326aa',
				# Export break_all_grabs() within Quartz backend
				'http://git.gnome.org/browse/gtk+/patch/?id=ac4f3be6a5a6672708af8fe732b932fd1e1d8beb',
				# [quartz] Fix manual resizing of windows
				'http://git.gnome.org/browse/gtk+/patch/?id=5f25687104f77aba310ac32c35d263f9d565d983',
				# quartz: fix coordinates for synthesized event
				'http://git.gnome.org/browse/gtk+/patch/?id=f91c525fe23a71abe389746bc5560bfe507ae5cb',
				# quartz: properly handle the given hotspot position
				'http://git.gnome.org/browse/gtk+/patch/?id=698aba575c506c81dc0f05b1224f94b54a83c5c4',

				# attempt to work around 2158 - [GTK] crash triggering context menu
				# also prints some warnings that may help to debug the real issue
				'https://bugzilla.xamarin.com/attachment.cgi?id=1644',

				# Bug 2698 - [GTK] Clipboard gets cleared after closing Monodevelop
				'https://bugzilla.xamarin.com/attachment.cgi?id=1722',

				# Backport of gdk_screen_get_monitor_workarea
				# Tooltip etc now honor menu and dock when positioning
				'patches/gtk-monitor-workarea.patch',

				# Embedded NSViews
				'patches/gtk-embedded-nsview/0001-gtk-add-new-widget-GtkNSView-which-alows-to-embed-an.patch',
				'patches/gtk-embedded-nsview/0002-quartz-return-events-on-embedded-foreign-NSViews-bac.patch',
				'patches/gtk-embedded-nsview/0003-gdk-add-signal-GdkWindow-native-child-event.patch',
				'patches/gtk-embedded-nsview/0004-tests-add-a-GtkEntry-to-testnsview-so-we-can-test-fo.patch',
				'patches/gtk-embedded-nsview/0005-gtk-connect-to-GdkWindow-native-child-event-to-imple.patch',

			])

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

	def install(self):
		Package.install(self)
		self.install_gtkrc ()

	def install_gtkrc(self):
		origin = os.path.join (self.package_dest_dir (), os.path.basename (self.sources[1]))
		destdir = os.path.join (self.prefix, "etc", "gtk-2.0")
		if not os.path.exists (destdir):
			os.makedirs(destdir)
		self.sh('cp %s %s' % (origin, destdir))

GtkPackage ()
