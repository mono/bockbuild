class GtkPackage (GnomeXzPackage):
	def __init__ (self):
		GnomeXzPackage.__init__ (self, 'gtk+',
			version_major = '2.24',
			version_minor = '13',
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

				#post 2.24.13 patches
				# Fix garbage content when windows are initially mapped
				'http://git.gnome.org/browse/gtk+/patch/?id=92ea94af5f1a4d0970628b58997192ccf74cab36',
				# quartz: Actually use the window background PATTERN color
				'http://git.gnome.org/browse/gtk+/patch/?id=0e42cf81f1dad319489e447c6c4e640bed2ab915',
				# quartz: _gdk_quartz_gc_update_cg_context(): the minimum line width is 1.0
				'http://git.gnome.org/browse/gtk+/patch/?id=5934ad2e22dd04deb823abebeb2815f73522fd5d',
				# quartz: move SPLASHSCREEN-hinted windows to NSStatusWindowLevel
				'http://git.gnome.org/browse/gtk+/patch/?id=47f0e3f1e1cd6b0ae61ec7ced48cc9802f1a95a4',
				# quartz: filter out button press events on the window frame
				'http://git.gnome.org/browse/gtk+/patch/?id=43e1354b71640d3fb7a47b997a436dc65bbd922f',
				# quartz: add _gdk_quartz_window_set_needs_display_in_region
				'http://git.gnome.org/browse/gtk+/patch/?id=4d01c56d8953d2b9f30625c32a5a8f223c0539d0',
				# quartz: correct deficiencies in the gdk_draw_drawable() implementationgtk
				'http://git.gnome.org/browse/gtk+/patch/?id=e982461ad63c7ce1f052378dbf5c28f7208f396a',

				# smooth scrolling, scrollbars, overscroll
				'patches/gtk-scrolling/0001-Bug-672193-windows-including-menus-shown-multiple-ti.patch',
				'patches/gtk-scrolling/0004-gtk-paint-only-the-exposed-region-in-gdk_window_expo.patch',
				'patches/gtk-scrolling/0005-Implement-gtk-enable-overlay-scrollbars-GtkSetting.patch',
				'patches/gtk-scrolling/0006-Smooth-scrolling.patch',
				'patches/gtk-scrolling/0007-gtk-Add-a-way-to-do-event-capture.patch',
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
				'patches/gtk-scrolling/0027-quartz-always-send-GDK_NOTIFY_NONLINEAR-crossing-eve.patch',
				'patches/gtk-scrolling/overlay-scrollbar-makefile-patch.diff',

				# make new modifier behviour opt-in, so as not to break old versions of MonoDevelop
				'patches/gdk-quartz-set-fix-modifiers-hack-v3.patch',

				# attempt to work around 2158 - [GTK] crash triggering context menu
				# also prints some warnings that may help to debug the real issue
				'https://bugzilla.xamarin.com/attachment.cgi?id=1644',

				# Backport of gdk_screen_get_monitor_workarea
				# Tooltip etc now honor menu and dock when positioning
				'patches/gtk-monitor-workarea.patch',

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
