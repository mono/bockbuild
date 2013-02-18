class GtkPackage (GnomeGitPackage):
	def __init__ (self):
		GnomeGitPackage.__init__ (self, 'gtk+', '2.24', '0004fe6cd44bf1033f606c0f9fe9a3784eeb4e73',
			configure_flags = [
				'--with-gdktarget=%{gdk_target}',
#				'--disable-cups',
			]
		)
		self.gdk_target = 'x11'

		if Package.profile.name == 'darwin':
			self.gdk_target = 'quartz'
			self.sources.extend ([
				# Custom gtkrc
				'patches/gtkrc',

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
				'patches/gtk-scrolling/0028-Hackish-fix-for-bug-8493-Min-size-of-GtkScrolledWind.patch',
				'patches/gtk-scrolling/0029-quartz-add-gdk_screen_-and-gdk_window_get_scale_fact.patch',
				'patches/gtk-scrolling/0030-gtk-add-gtk_widget_get_scale_factor.patch',
				'patches/gtk-scrolling/0031-iconfactory-Add-_scaled-variants.patch',
				'patches/gtk-scrolling/0032-widget-Add-_scaled-variants-for-icon-rendering.patch',
				'patches/gtk-scrolling/0033-image-Use-scaled-icons-on-windows-with-a-scaling-fac.patch',
				'patches/gtk-scrolling/0034-cellrendererpixbuf-Use-scaled-icons-on-windows-with-.patch',
				'patches/gtk-scrolling/0035-entry-Use-scaled-icons-on-windows-with-a-scale-facto.patch',
				'patches/gtk-scrolling/0036-gtk-use-gtk_widget_get_scale_factor-and-cache-scaled.patch',
				'patches/gtk-scrolling/fix-overlay-scrollbar-grab.diff',
				'patches/gtk-scrolling/fix-mouse-events-1.patch',
				'patches/gtk-scrolling/fix-mouse-events-2.patch',


				# make new modifier behviour opt-in, so as not to break old versions of MonoDevelop
				'patches/gdk-quartz-set-fix-modifiers-hack-v3.patch',

				# attempt to work around 2158 - [GTK] crash triggering context menu
				# also prints some warnings that may help to debug the real issue
				'https://bugzilla.xamarin.com/attachment.cgi?id=1644',

				# Embedded NSViews
				'patches/gtk-embedded-nsview/0001-quartz-return-events-on-embedded-foreign-NSViews-bac.patch',
				'patches/gtk-embedded-nsview/0002-gtk-add-new-widget-GtkNSView-which-alows-to-embed-an.patch',
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
