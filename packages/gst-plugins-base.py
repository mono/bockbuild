class GstPluginsBasePackage (GstreamerPackage):
	def __init__ (self):
		GstreamerPackage.__init__ (self, 'gstreamer', 'gst-plugins-base',
			'0.10.36', configure_flags = [
				'--disable-gtk-doc',
				'--disable-gio',
				'--disable-gnome_vfs',
				'--disable-pango'
			]
		)

		# FIXME: these should be passed on the Linux profile
		# when we do away with xvideo/xoverlay and replace
		# with Clutter and Cairo
		if Package.profile.name == 'darwin':
			self.configure_flags.extend ([
				'--disable-x',
				'--disable-xvideo',
				'--disable-xshm'
			])

GstPluginsBasePackage ()
