class GtkPackage (GnomePackage):
	def __init__ (self):
		GnomePackage.__init__ (self, 'gtk+',
			version_major = '2.24',
			version_minor = '5',
			configure_flags = [
				'--with-gdktarget=%{gdk_target}',
				'--disable-cups',
			]
		)

		self.gdk_target = 'x11'
		if Package.profile.name == 'darwin':
			self.gdk_target = 'quartz'
			self.sources.extend ([
				# input_window_destroy/input_window_crossing stubs
				'http://github.com/jralls/gtk-osx-build/raw/master/patches/gdk-quartz-input-window.patch',

				# Bug 346609 - [PATCH] Quartz backend has no support for one-button mice
				#	https://bugzilla.gnome.org/show_bug.cgi?id=346609
				'http://git.dronelabs.com/gtk+/patch/?id=729cbea7a2b27c4b8f2062316c0f406ab4c01dac',

				# Bug 655074 - [PATCH] Fix crash with undecorated windows on MacOS Lion
				#	https://bugzilla.gnome.org/show_bug.cgi?id=655074
				'https://bugzilla.gnome.org/attachment.cgi?id=192427',

				# patches from gtk-2-24-quartz branch

				# Handle alt/option modifier key with GDK_MOD5_MASK so that it's recognized as a
				# modifier key for accelerators.
				'http://git.gnome.org/browse/gtk+/patch?id=689ee935c157d63df8ce11d9e8ce2f8da36da2cd'

				# Implement relocatable paths for quartz, similar to those in Win32
				'http://git.gnome.org/browse/gtk+/patch?id=d15c82a4652cf23be5e6c40473c4b7302b513dd6',

				# Enable using those standard mac deadkeys which are supported by the simple IM.
				'http://git.gnome.org/browse/gtk+/patch?id=7fb399d44f5ca741e3257a1f03d978e18ef2fd1a',
				
# these patches break linking
#				# Bug 571582: GtkSelection implementation for quartz.
#				'http://git.gnome.org/browse/gtk+/patch?id=8231c7d1c292c3d24181b42c464c266fa3283a9a',
#
#				# Bug 628396: Gtk build fails because of objective-c elements
#				'http://git.gnome.org/browse/gtk+/patch?id=e4b0cbe3184af2d4472f29c61d0bf6e93747d78e',

				# Return a NULL context and don't queue up another drag_begin_idle rather than
				# asserting if the static drag_context isn't NULL (meaning that a drag is already
				# in progress).
				'http://git.gnome.org/browse/gtk+/patch?id=8bec04aed6112c6190efa473ce0aef742b13f776',

				# Move the retrieval of the NSEvent to the beginning of drag_begin_internal in a
				# (probably vain) effort to reduce the race condition caused by deferring actually
				# starting the drag until idle time.
				'http://git.gnome.org/browse/gtk+/patch?id=609548d995c93ac1d161135be60c012335f125f7',

#				# Force an ownerChanged notification when we destroy a widget with a selection, and
#				# act on the notification in DnD. This should prevent CF trying to retrieve any
#				# deferred pasteboard types later, and DnD crashing if it does.
#				'http://git.gnome.org/browse/gtk+/patch?id=de82a1d0aa03750864af17a9fe34011d22da8c80',

				# Fix refresh of static autorelease_pool so that it doesn't happen in gtk-nested loops.
				'http://git.gnome.org/browse/gtk+/patch?id=b5046c24ed0681bf0bbf1d1e2872897f84eae06e',

				# Fix typo in gdk_event_check
				'http://git.gnome.org/browse/gtk+/patch?id=90c970b541d32631c22ca1c2ddfeee4188a8f278',

				# Use a synthesized mouse nsevent to start a drag instead of grabbing the most
				# recent event from the nswindow (which may well not be the right event).
				'http://git.gnome.org/browse/gtk+/patch?id=c297c31732216be7d60b3b11244855d7f7f98003',
			])

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (2, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

GtkPackage ()
