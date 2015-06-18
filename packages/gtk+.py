class GtkPackage (GnomeGitPackage):
	def __init__ (self):
		GnomeGitPackage.__init__ (self, 'gtk+', '2.24', '280fc402be5fb46b66bcd32056963bb1afb8b54b',
			configure_flags = [
				'--with-gdktarget=%{gdk_target}',
#				'--disable-cups',
			]
		)
		self.gdk_target = 'x11'

		if Package.profile.name == 'darwin':
			self.gdk_target = 'quartz'

			default_patch_options = ' -p1 --ignore-whitespace '
			self.sources.extend ([
				# Custom gtkrc
				'patches/gtkrc',

				# smooth scrolling, scrollbars, overscroll, retina, gtknsview
				Patch('patches/gtk/0001-Add-invariant-that-a-child-is-unmapped-if-parent-is-.patch', options = default_patch_options),
				Patch('patches/gtk/0002-Maintain-map-unmap-invariants-in-GtkRecentChooserDia.patch', options = default_patch_options),
				Patch('patches/gtk/0003-GtkPlug-preserve-map-unmap-invariants.patch', options = default_patch_options),
				Patch('patches/gtk/0004-Add-gdk_screen_get_monitor_workarea-and-use-it-all-o.patch', options = default_patch_options),
				Patch('patches/gtk/0005-gtk-don-t-scroll-combo-box-menus-if-less-than-3-item.patch', options = default_patch_options),
				Patch('patches/gtk/0006-gtk-paint-only-the-exposed-region-in-gdk_window_expo.patch', options = default_patch_options),
				Patch('patches/gtk/0007-Implement-gtk-enable-overlay-scrollbars-GtkSetting.patch', options = default_patch_options),
				Patch('patches/gtk/0008-Smooth-scrolling.patch', options = default_patch_options),
				Patch('patches/gtk/0009-gtk-Add-a-way-to-do-event-capture.patch', options = default_patch_options),
				Patch('patches/gtk/0010-gtk-don-t-let-insensitive-children-eat-scroll-events.patch', options = default_patch_options),
				Patch('patches/gtk/0011-scrolledwindow-Kinetic-scrolling-support.patch', options = default_patch_options),
				Patch('patches/gtk/0012-gtk-paint-to-the-right-windows-in-gtk_scrolled_windo.patch', options = default_patch_options),
				Patch('patches/gtk/0013-GtkScrolledWindow-add-overlay-scrollbars.patch', options = default_patch_options),
				Patch('patches/gtk/0014-gtk-add-event-handling-to-GtkScrolledWindow-s-overla.patch', options = default_patch_options),
				Patch('patches/gtk/0015-Use-gtk-enable-overlay-scrollbars-in-GtkScrolledWind.patch', options = default_patch_options),
				Patch('patches/gtk/0016-gtk-correctly-handle-toggling-of-the-scrollbar-visib.patch', options = default_patch_options),
				Patch('patches/gtk/0017-gtk-handle-gtk-primary-button-warps-slider-for-the-o.patch', options = default_patch_options),
				Patch('patches/gtk/0018-Introduce-phase-field-in-GdkEventScroll.patch', options = default_patch_options),
				Patch('patches/gtk/0019-Add-hack-to-lock-flow-of-scroll-events-to-window-whe.patch', options = default_patch_options),
				Patch('patches/gtk/0020-Introduce-a-background-window.patch', options = default_patch_options),
				Patch('patches/gtk/0021-Make-scrolled-window-work-well-with-Mac-touchpad.patch', options = default_patch_options),
				Patch('patches/gtk/0022-Use-start-end-phase-in-event-handling.patch', options = default_patch_options),
				Patch('patches/gtk/0023-Improve-overshooting-behavior.patch', options = default_patch_options),
				Patch('patches/gtk/0024-Cancel-out-smaller-delta-component.patch', options = default_patch_options),
				Patch('patches/gtk/0025-quartz-Add-a-dummy-NSView-serving-as-layer-view.patch', options = default_patch_options),
				Patch('patches/gtk/0026-gtk-port-overlay-scrollbars-to-native-CALayers.patch', options = default_patch_options),
				Patch('patches/gtk/0027-Refrain-from-starting-fading-out-while-a-gesture-is-.patch', options = default_patch_options),
				Patch('patches/gtk/0028-gtk-don-t-show-the-olverlay-scrollbars-if-only-the-s.patch', options = default_patch_options),
				Patch('patches/gtk/0029-Reclamp-unclamped-adjustments-after-resize.patch', options = default_patch_options),
				Patch('patches/gtk/0030-gtk-fix-size_request-of-scrolled-window.patch', options = default_patch_options),
				Patch('patches/gtk/0031-Hackish-fix-for-bug-8493-Min-size-of-GtkScrolledWind.patch', options = default_patch_options),
				Patch('patches/gtk/0032-Add-momentum_phase-to-GdkEventScroll.patch', options = default_patch_options),
				Patch('patches/gtk/0033-Never-intervene-in-the-event-stream-for-legacy-mice.patch', options = default_patch_options),
				Patch('patches/gtk/0034-Do-not-start-overshooting-for-legacy-mouse-scroll-ev.patch', options = default_patch_options),
				Patch('patches/gtk/0035-gtk-remove-the-overlay-scrollbar-grab-on-unrealize.patch', options = default_patch_options),
				Patch('patches/gtk/0036-gtk-add-GtkScrolledWindow-API-to-disable-overshoot-p.patch', options = default_patch_options),
				Patch('patches/gtk/0037-quartz-return-events-on-embedded-foreign-NSViews-bac.patch', options = default_patch_options),
				Patch('patches/gtk/0038-quartz-don-t-forward-events-to-the-toplevel-nswindow.patch', options = default_patch_options),
				Patch('patches/gtk/0039-gdk-add-a-move-native-children-signal-to-GdkWindow.patch', options = default_patch_options),
				Patch('patches/gtk/0040-gtk-add-new-widget-GtkNSView-which-alows-to-embed-an.patch', options = default_patch_options),
				Patch('patches/gtk/0041-tests-add-a-notebook-to-testnsview.c.patch', options = default_patch_options),
				Patch('patches/gtk/0042-gtk-connect-GtkNSView-to-move-native-children-and-re.patch', options = default_patch_options),
				Patch('patches/gtk/0043-tests-add-a-scrolled-window-test-widget-to-testnsvie.patch', options = default_patch_options),
				Patch('patches/gtk/0044-gtknsview-clip-drawRect-to-a-parent-GtkViewport-s-wi.patch', options = default_patch_options),
				Patch('patches/gtk/0045-gtk-clip-NSViews-to-the-scrolled-window-s-overshoot_.patch', options = default_patch_options),
				Patch('patches/gtk/0046-gtk-implement-clipping-to-multiple-parent-viewports-.patch', options = default_patch_options),
				Patch('patches/gtk/0047-gtk-first-attempt-to-also-clip-NSWindow-s-field-edit.patch', options = default_patch_options),
				Patch('patches/gtk/0048-gtk-also-clip-the-NSView-s-subviews.patch', options = default_patch_options),
				Patch('patches/gtk/0049-nsview-also-swizzle-DidAddSubview-and-clip-all-subvi.patch', options = default_patch_options),
				Patch('patches/gtk/0050-nsview-clip-text-field-cursor-drawing.patch', options = default_patch_options),
				Patch('patches/gtk/0051-nsview-factor-out-almost-all-code-from-the-overridde.patch', options = default_patch_options),
				Patch('patches/gtk/0052-nsview-also-focus-the-GtkNSView-if-a-focussable-subv.patch', options = default_patch_options),
				Patch('patches/gtk/0053-gtk-add-an-overlay-policy-API-to-GtkScrolledWindow.patch', options = default_patch_options),
				Patch('patches/gtk/0054-quartz-add-gdk_screen_-and-gdk_window_get_scale_fact.patch', options = default_patch_options),
				Patch('patches/gtk/0055-gtk-add-gtk_widget_get_scale_factor.patch', options = default_patch_options),
				Patch('patches/gtk/0056-iconfactory-Add-_scaled-variants.patch', options = default_patch_options),
				Patch('patches/gtk/0057-widget-Add-_scaled-variants-for-icon-rendering.patch', options = default_patch_options),
				Patch('patches/gtk/0058-icontheme-Add-support-for-high-resolution-icons.patch', options = default_patch_options),
				Patch('patches/gtk/0059-iconfactory-Add-scale-info-to-GtkIconSource.patch', options = default_patch_options),
				Patch('patches/gtk/0060-iconfactory-Add-gtk_cairo_set_source_icon_set.patch', options = default_patch_options),
				Patch('patches/gtk/0061-image-Use-scaled-icons-on-windows-with-a-scaling-fac.patch', options = default_patch_options),
				Patch('patches/gtk/0062-cellrendererpixbuf-Use-scaled-icons-on-windows-with-.patch', options = default_patch_options),
				Patch('patches/gtk/0063-entry-Use-scaled-icons-on-windows-with-a-scale-facto.patch', options = default_patch_options),
				Patch('patches/gtk/0064-gdk-Lookup-double-scaled-variants-on-pixbufs.patch', options = default_patch_options),
				Patch('patches/gtk/0065-Make-usual-calls-to-get-a-GdkPixbuf-attach-a-2x-vari.patch', options = default_patch_options),
				Patch('patches/gtk/0066-cellrendererpixbuf-let-2x-variants-go-through-pixel-.patch', options = default_patch_options),
				Patch('patches/gtk/0067-quartz-Make-event-loop-deal-with-recursive-poll-invo.patch', options = default_patch_options),
				Patch('patches/gtk/0068-nsview-implement-a-few-text-view-command-accelerator.patch', options = default_patch_options),
				Patch('patches/gtk/0069-menu-scrolling.patch', options = default_patch_options),
				Patch('patches/gtk/0070-tooltips-focus.patch', options = default_patch_options),
				Patch('patches/gtk/0071-light-and-dark-overlay-scrollbars.patch', options = default_patch_options),
				Patch('patches/gtk/0072-let-global-keyboard-shortcuts-pass-through.patch', options = default_patch_options),
				Patch('patches/gtk/0073-disable-combobox-scrolling.patch', options = default_patch_options),
				Patch('patches/gtk/0074-fix-NULL-pointer-in-clipboard.patch', options = default_patch_options),
				Patch('patches/gtk/0075-filechooserwidget-location-entry-activation.patch', options = default_patch_options),
				Patch('patches/gtk/0076-iconfactory-treat-gt-1-0-icons-as-2-0.patch', options = default_patch_options),

				# Bug 702841 - GdkQuartz does not distinguish Eisu, Kana and Space keys on Japanese keyrboard
				# https://bugzilla.gnome.org/show_bug.cgi?id=702841
				Patch('patches/gtk/bgo702841-fix-kana-eisu-keys.patch', options = default_patch_options),

				# make new modifier behviour opt-in, so as not to break old versions of MonoDevelop
				Patch('patches/gdk-quartz-set-fix-modifiers-hack-v3.patch', options = default_patch_options),

				# attempt to work around 2158 - [GTK] crash triggering context menu
				# also prints some warnings that may help to debug the real issue
				# https://bugzilla.xamarin.com/attachment.cgi?id=1644
				Patch('patches/gtk/bxc2158_workaround_crash_triggering_context_menu.patch', options = default_patch_options),

				# Zoom, rotate, swipe events
				Patch('patches/gtk-gestures.patch', options = default_patch_options),

				# Fix gtk_window_begin_move_drag on Quartz
				Patch('patches/gtk-quartz-move-drag.patch', options = default_patch_options),

				# Bug 3457 - [GTK] Support more standard keyboard shortcuts in dialogs
				# https://bugzilla.xamarin.com/attachment.cgi?id=2240
				Patch('patches/gtk/bxc3457_more_standard_keyboard_shortcuts.patch', options = default_patch_options),

				# Bug  10256 - Mac window manipulation tools get confused by Xamarin Studio
				# https://bugzilla.xamarin.com/attachment.cgi?id=3465
				Patch('patches/gtk/bxc_10256_window_tools_get_confused.diff', options = default_patch_options),

#                                Patch('patches/gtk/gdk-pixmap-get-cgimage-2.patch', options = default_patch_options),

				# https://bugzilla.xamarin.com/show_bug.cgi?id=18157
				Patch('patches/gtk/gtk-check-grab_toplevel-is-destroyed.patch', options = default_patch_options),

				# https://bugzilla.xamarin.com/show_bug.cgi?id=18241
				# https://bugzilla.xamarin.com/show_bug.cgi?id=17631
				# https://bugzilla.xamarin.com/show_bug.cgi?id=17692
				Patch('patches/gtk/gtk-imquartz-defer-signals-in-output_result.patch', options = default_patch_options),

				# https://bugzilla.xamarin.com/show_bug.cgi?id=17401
				Patch('patches/gtk/gtknsview-defer-map-and-lock-in-clipping.patch', options = default_patch_options),
				Patch('patches/gtk/gtknsview-timeout-fix.patch', options = default_patch_options),

                                Patch('patches/gtk/nsview-embedding.patch', options = default_patch_options),

                                Patch('patches/gtk/enable-swizzle-property.patch', options = default_patch_options),

				# https://bugzilla.xamarin.com/show_bug.cgi?id=12618
				Patch('patches/gtk/disable-eye-dropper.patch', options = default_patch_options),

				# https://bugzilla.xamarin.com/show_bug.cgi?id=13100
				Patch('patches/gtk/flip-command-mask-between-mod1-and-mod2.patch', options = default_patch_options),
				Patch('patches/gtk/nsview-embedding-fix-keyboard-routing.patch', options = default_patch_options),
				Patch('patches/gtk/nsview-check-for-superview.patch', options = default_patch_options),

				Patch('patches/gtk/gtknsview-forward-cmdz-to-textview-undo-manager.patch', options = default_patch_options),

				# https://bugzilla.xamarin.com/show_bug.cgi?id=20732
				Patch('patches/gtk/embedded-nstextview-has-focus.patch', options = default_patch_options),
				Patch('patches/gtk/remove-demos-from-build.patch', options = default_patch_options),

				# This fixes an issue in where in some situations the user needed
				# to click a native text entry twice in order to be able to focus it.
				Patch('patches/gtk/gtknsview-only-unset-first-responder-if-it-is-our-view.patch', options = default_patch_options),

				# For the test framework to be able to traverse down the NSView hierarchy
				Patch('patches/gtk/gtknsview-getter.patch', options = default_patch_options),

				# This is hacky, but the designer needs a way to handle drag events
				# from Xamarin.Mac and GTK is eating them. If a better solution is found
				# we should remove this.
				# https://bugzilla.xamarin.com/show_bug.cgi?id=29301
				Patch('patches/gtk/gtk-yield-mouse-events-to-cocoa.patch', options = default_patch_options),

				# https://bugzilla.xamarin.com/show_bug.cgi?id=29301#c3
				Patch('patches/gtk/gtknsview-fix-invalid-casts.patch', options = default_patch_options),

				# https://bugzilla.xamarin.com/show_bug.cgi?id=29001
				Patch('patches/gtk/quartz-call-undo-redo-on-cmdz.patch', options = default_patch_options),
			])

		self.make = "GDK_PIXBUF_MODULEDIR=%{staged_prefix}/lib/gdk-pixbuf-2.0/2.10.0/loaders GDK_PIXBUF_MODULE_FILE=%{staged_prefix}/lib/gdk-pixbuf-2.0/2.10.0/loaders.cache " + self.make

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (2, len (self.local_sources)):
				self.sh ('patch -p1 --ignore-whitespace < "%{local_sources[' + str (p) + ']}"')

	def install(self):
		Package.install(self)
		if Package.profile.name == 'darwin':
			self.install_gtkrc ()

	def install_gtkrc(self):
		gtkrc = self.local_sources[1]
		destdir = os.path.join (self.staged_prefix, "etc", "gtk-2.0")
		if not os.path.exists (destdir):
			os.makedirs(destdir)
		self.sh('cp %s %s' % (gtkrc, destdir))

GtkPackage ()
