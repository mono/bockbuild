import os
from bockbuild.darwinprofile import DarwinProfile

class MonoDevelopMacDevPackages:
	def __init__ (self):
		# Toolchain
		self.packages.extend ([
			'xz.py',
			'tar.py',
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
			'libtiff.py',
			'libxml2.py',
			'freetype.py',
			'fontconfig.py',
			'pixman.py',
			'cairo.py',
			'libffi.py',
			'glib.py',
			'pango.py',
			'atk.py',
			'intltool.py',
			'gdk-pixbuf.py',
			'gtk+.py',
			'libglade.py',
		])

		# Theme
		self.packages.extend ([
			'libcroco.py',
			'librsvg.py',
			'hicolor-icon-theme.py',
			'gtk-engines.py',
			'murrine.py',
			'gtk-quartz-engine.py'
		])

		# Mono
		self.packages.extend ([
			'mono.py',
			'gtk-sharp.py',
			'mono-addins.py',
		])

		self.packages = [os.path.join ('..', '..', 'packages', p)
			for p in self.packages]
