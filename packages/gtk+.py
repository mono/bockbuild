class GtkPackage (GnomeXzPackage):
	def __init__ (self):
		GnomeXzPackage.__init__ (self, 'gtk+',
			version_major = '2.24',
			version_minor = '14',
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
				# Custom gtkrc
				'patches/gtkrc',

				#post 2.24.14 patches
				# quartz: fix crash in the recent clipboard "fix", and really fix it
				'http://git.gnome.org/browse/gtk+/patch/?id=4a8df7a33c298d22bf78b947d0e861fc03ec70e1',
				# gtk: fix scrolling in modal dialogs when event_widget is insensitive
				'http://git.gnome.org/browse/gtk+/patch/?id=31ae1a0b5bb257c86cc2393e065ded8506b4ef4a',
				# quartz: make setting_same_owner member of GtkClipboardOwner @public
				'http://git.gnome.org/browse/gtk+/patch/?id=e3e055f8551ac8ee033f361261c849c612554184',
				# quartz: don't call a NULL get_func() in gtk_clipboard_store()
				'http://git.gnome.org/browse/gtk+/patch/?id=f1c105b94fc3c3572a234c93c47252a3ff82218b',
				# Move single-include guards inside include guards
				'http://git.gnome.org/browse/gtk+/patch/?id=1f0f3994694ec3f1baa43932c186db78814b2abd',
				# quartz: ensure window being (un)fullscreened is visible
				'http://git.gnome.org/browse/gtk+/patch/?id=62f1d871b70a8e08b899942827386d6f3222c986',
				# quartz: make sure all old properties are set on the new toplevel
				'http://git.gnome.org/browse/gtk+/patch/?id=a8008b796f14444dff3ac46af884238fc4f214f6',
				# quartz: Make sure the old toplevel is closed on recreation
				'http://git.gnome.org/browse/gtk+/patch/?id=30deba453a045107eadd4deea572e29192c298c1',
				# quartz: retain content view when switching over toplevel
				'http://git.gnome.org/browse/gtk+/patch/?id=184407309f83a06b9215c8123091263d483edc8b',
				# quartz: really don't call a NULL function in gtk_clipboard_store()
				'http://git.gnome.org/browse/gtk+/patch/?id=bc3f1893aa26761c0009ddc993b48623bcfbe4ed',

				# smooth scrolling, scrollbars, overscroll
				'patches/gtk-scrolling/0001-Add-gdk_screen_get_monitor_workarea-and-use-it-all-o.patch',
				'patches/gtk-scrolling/0002-gtk-don-t-scroll-combo-box-menus-if-less-than-3-item.patch',
				'patches/gtk-scrolling/0003-gtk-paint-only-the-exposed-region-in-gdk_window_expo.patch',
				'patches/gtk-scrolling/0004-Implement-gtk-enable-overlay-scrollbars-GtkSetting.patch',
				'patches/gtk-scrolling/0005-Smooth-scrolling.patch',
				'patches/gtk-scrolling/0006-gtk-Add-a-way-to-do-event-capture.patch',
				'patches/gtk-scrolling/0007-gtk-don-t-let-insensitive-children-eat-scroll-events.patch',
				'patches/gtk-scrolling/0008-scrolledwindow-Kinetic-scrolling-support.patch',
				'patches/gtk-scrolling/0009-gtk-paint-to-the-right-windows-in-gtk_scrolled_windo.patch',
				'patches/gtk-scrolling/0010-GtkScrolledWindow-add-overlay-scrollbars.patch',
				'patches/gtk-scrolling/0011-gtk-add-event-handling-to-GtkScrolledWindow-s-overla.patch',
				'patches/gtk-scrolling/0012-Use-gtk-enable-overlay-scrollbars-in-GtkScrolledWind.patch',
				'patches/gtk-scrolling/0013-gtk-correctly-handle-toggling-of-the-scrollbar-visib.patch',
				'patches/gtk-scrolling/0014-gtk-handle-gtk-primary-button-warps-slider-for-the-o.patch',
				'patches/gtk-scrolling/0015-Introduce-phase-field-in-GdkEventScroll.patch',
				'patches/gtk-scrolling/0016-Add-hack-to-lock-flow-of-scroll-events-to-window-whe.patch',
				'patches/gtk-scrolling/0017-Introduce-a-background-window.patch',
				'patches/gtk-scrolling/0018-Make-scrolled-window-work-well-with-Mac-touchpad.patch',
				'patches/gtk-scrolling/0019-Use-start-end-phase-in-event-handling.patch',
				'patches/gtk-scrolling/0020-Improve-overshooting-behavior.patch',
				'patches/gtk-scrolling/0021-Cancel-out-smaller-delta-component.patch',
				'patches/gtk-scrolling/0022-quartz-Add-a-dummy-NSView-serving-as-layer-view.patch',
				'patches/gtk-scrolling/0023-gtk-port-overlay-scrollbars-to-native-CALayers.patch',
				'patches/gtk-scrolling/0024-Refrain-from-starting-fading-out-while-a-gesture-is-.patch',
				'patches/gtk-scrolling/0025-gtk-don-t-show-the-olverlay-scrollbars-if-only-the-s.patch',
				'patches/gtk-scrolling/0026-Reclamp-unclamped-adjustments-after-resize.patch',
				'patches/gtk-scrolling/0027-gtk-fix-size_request-of-scrolled-window.patch',
				'patches/gtk-scrolling/overlay-scrollbar-makefile-patch.diff',
				'patches/gtk-scrolling/fix-overlay-scrollbar-grab.diff',

				# make new modifier behviour opt-in, so as not to break old versions of MonoDevelop
				'patches/gdk-quartz-set-fix-modifiers-hack-v3.patch',

				# attempt to work around 2158 - [GTK] crash triggering context menu
				# also prints some warnings that may help to debug the real issue
				'https://bugzilla.xamarin.com/attachment.cgi?id=1644',

				# Embedded NSViews
				'patches/gtk-embedded-nsview/0001-gtk-add-new-widget-GtkNSView-which-alows-to-embed-an.patch',
				'patches/gtk-embedded-nsview/0002-quartz-return-events-on-embedded-foreign-NSViews-bac.patch',
				'patches/gtk-embedded-nsview/0003-gdk-add-signal-GdkWindow-native-child-event.patch',
				'patches/gtk-embedded-nsview/0004-tests-add-a-GtkEntry-to-testnsview-so-we-can-test-fo.patch',
				'patches/gtk-embedded-nsview/0005-gtk-connect-to-GdkWindow-native-child-event-to-imple.patch',
				'patches/gtk-embedded-nsview/fix-for-embedded-nsviews.patch',

				# Zoom, rotate, swipe events
				'patches/gtk-gestures.patch',

				# Fix gtk_window_begin_move_drag on Quartz
				'patches/gtk-quartz-move-drag.patch',

				# Bug 6156 - [gtk] Quitting the application with unsaved file and answering Cancel results in crash
				'https://bugzilla.xamarin.com/attachment.cgi?id=2214',

				# Bug 3457 - [GTK] Support more standard keyboard shortcuts in dialogs
				'https://bugzilla.xamarin.com/attachment.cgi?id=2240',
			])

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (2, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

	def install(self):
		Package.install(self)
		if Package.profile.name == 'darwin':
			self.install_gtkrc ()

	def install_gtkrc(self):
		origin = os.path.join (self.package_dest_dir (), os.path.basename (self.sources[1]))
		destdir = os.path.join (self.prefix, "etc", "gtk-2.0")
		if not os.path.exists (destdir):
			os.makedirs(destdir)
		self.sh('cp %s %s' % (origin, destdir))

GtkPackage ()
