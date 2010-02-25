from bockbuild.darwinprofile import DarwinProfile

class BansheePackages:
	def __init__ (self):
		# Toolchain
		self.packages.extend ([
			'packages/autoconf.py',
			'packages/automake.py',
			'packages/libtool.py',
			'packages/gettext.py',
			'packages/pkg-config.py'
		])

		# Base Libraries
		self.packages.extend ([
			# 'packages/libiconv.py',
			'packages/libpng.py',
			'packages/libjpeg.py',
			'packages/libxml2.py',
			'packages/freetype.py',
			'packages/fontconfig.py',
			'packages/pixman.py',
			'packages/cairo.py',
			'packages/glib.py',
			'packages/pango.py',
			'packages/atk.py',
			'packages/intltool.py',
			'packages/gtk+.py',
			'packages/gconf-dummy.py',
			'packages/libproxy.py',
			'packages/libsoup.py',
			'packages/sqlite.py'
		])

		# Theme
		self.packages.extend ([
			'packages/librsvg.py',
			'packages/icon-naming-utils.py',
			'packages/hicolor-icon-theme.py',
			'packages/tango-icon-theme.py',
			'packages/murrine.py'
		])

		# Codecs
		self.packages.extend ([
			'packages/libogg.py',
			'packages/libvorbis.py',
			'packages/flac.py',
			'packages/libtheora.py',
			'packages/speex.py',
			'packages/wavpack.py',
			'packages/taglib.py',
		])

		# GStreamer
		self.packages.extend ([
			'packages/liboil.py',
			'packages/gstreamer.py',
			'packages/gst-plugins-base.py',
			'packages/gst-plugins-good.py'
		])

		if isinstance (self, DarwinProfile):
			self.packages.extend ([
				'packages/gst-plugins-bad.py',
				'packages/gst-plugins-ugly.py'
			])

		# Mono
		self.packages.extend ([
			'packages/mono.py',
			'packages/gtk-sharp.py',
			'packages/mono-addins.py',
			'packages/ndesk-dbus.py',
			'packages/ndesk-dbus-glib.py',
			'packages/taglib-sharp.py'
		])

		if isinstance (self, DarwinProfile):
			self.packages.extend ([
				'packages/monobjc.py',
				'packages/ige-mac-integration.py'
			])

		if self.cmd_options.release_build:
			self.packages.append ('packages/banshee.py')
