import os
from bockbuild.darwinprofile import DarwinProfile

class MonoReleasePackages:
	def __init__(self):

		# Toolchain
		self.packages.extend([
				# 'autoconf.py',
				# 'automake.py',
				# 'libtool.py', 
				'xz.py',
				'tar.py',
				'gettext.py',
				'pkg-config.py'
				])

		# # Base Libraries
		self.packages.extend([
				'libpng.py',
				'libjpeg.py',
				'libtiff.py',
				'libgif.py',
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
				'sqlite.py',
				'expat.py',
				'ige-mac-integration.py'
				])

		# # Theme
		self.packages.extend([
				'libcroco.py',
				'librsvg.py',
				'hicolor-icon-theme.py',
				'gtk-engines.py',
				# 'gtk-quartz-engine.py'
				])

		# Mono
		self.packages.extend([
				'mono-llvm.py',
				'mono-master.py',
				'libgdiplus.py',
				'xsp.py',
				'gtk-sharp-2.12-release.py',
				'boo.py',
				# 'nant.py',
				'ironlangs.py',
				'fsharp.py',
				'mono-addins.py',
				'mono-basic.py',
				])

		self.packages = [os.path.join('..', '..', 'packages', p) for p in self.packages]
