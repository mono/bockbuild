import os
from bockbuild.darwinprofile import DarwinProfile
from bockbuild.gnomeprofile import GnomeProfile
from bockbuild.glickprofile import GlickProfile

class BansheePackages:
	def __init__ (self):
		# Toolchain
		self.packages.extend ([
			'autoconf.py',
			'automake.py',
			'libtool.py',
			'gettext.py',
			'pkg-config.py'
		])

		# Base Libraries
		self.packages.extend ([
			'libpng.py',
			'libjpeg.py',
			'libxml2.py',
			'freetype.py',
			'fontconfig.py',
			'pixman.py',
			'cairo.py',
			'glib.py',
			'pango.py',
			'atk.py',
			'intltool.py',
			'gdk-pixbuf.py',
			'gtk+.py',
			'gconf-dummy.py',
			'libgpg-error.py',
			'libgcrypt.py',
			'gnutls.py',
			'glib-networking.py',
			'libsoup.py',
			'sqlite.py'
		])

		# WebKit
		self.packages.extend ([
			'gperf.py',
			'enchant.py',
			'libicu.py',
			'webkit.py'
		])

		# Theme
		self.packages.extend ([
			'librsvg.py',
			'icon-naming-utils.py',
			'hicolor-icon-theme.py',
			'tango-icon-theme.py',
			'murrine.py'
		])

		# Codecs
		self.packages.extend ([
			'libogg.py',
			'libvorbis.py',
			'flac.py',
			'libtheora.py',
			'speex.py',
			'wavpack.py',
			'taglib.py',
		])

		# GStreamer
		self.packages.extend ([
			'liboil.py',
			'gstreamer.py',
			'gst-plugins-base.py',
			'gst-plugins-good.py'
		])

		if isinstance (self, DarwinProfile):
			self.packages.extend ([
				'gst-plugins-bad.py',
				'gst-plugins-ugly.py'
			])

		# Mono
		self.packages.extend ([
			'mono.py',
			'gtk-sharp.py',
			'mono-addins.py',
			'ndesk-dbus.py',
			'ndesk-dbus-glib.py',
			'taglib-sharp.py',
		])

		if isinstance (self, DarwinProfile):
			self.packages.extend ([
				'monomac.py',
				'ige-mac-integration.py'
			])

		if self.cmd_options.release_build:
			self.packages.append ('banshee.py')

		self.packages = [os.path.join ('..', '..', 'packages', p)
			for p in self.packages]
