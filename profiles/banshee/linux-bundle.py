#!/usr/bin/python -B

import os
import sys

sys.path.append ('../..')

from bockbuild.glickprofile import GlickProfile
from linux import BansheeLinuxProfile

class BansheeLinuxBundleProfile (GlickProfile, BansheeLinuxProfile):
	def __init__ (self):
		BansheeLinuxProfile.__init__ (self)
		GlickProfile.__init__ (self)

		self_dir = os.path.realpath (os.path.dirname (sys.argv[0]))
		self.bundle_skeleton_dir = os.path.join (self_dir, 'skeleton.glick')
		self.bundle_output_dir = os.path.join (self_dir, 'bundle.glick')

		self.bundle_from_build = [
			'bin/mono',
			'lib/mono/2.0/gmcs.exe',
			'lib/mono/gac/Mono.Addins.CecilReflector',
			'lib/banshee-1',
			'lib/pango',
			'lib/gtk-2.0/2.10.0/loaders',
			'lib/gtk-2.0/2.10.0/engines',
			'lib/gtk-2.0/2.10.0/immodules',
			'lib/gdk-pixbuf-2.0/2.10.0/loaders',
			'lib/gdk-pixbuf-2.0/2.10.0/loaders.cache',
			'lib/gstreamer-0.10',
			'share/banshee-1',
			'share/locale',
			'etc/gtk-2.0',
			'etc/mono/config',
			'etc/mono/2.0/machine.config',
			'etc/mono/2.0/settings.map',
			'etc/pango/pango.modules',
			'share/icons/hicolor/index.theme',
			'share/icons/Tango/index.theme'
		]

		self.bundle_from_build.extend ([
			'share/icons/%s/%sx%s' % (theme, size, size)
				for size in [16, 22, 32, 48]
				for theme in ['hicolor', 'Tango']
		])

	def bundle (self):
		banshee_path = os.path.join (self.prefix, 'lib', 'banshee-1')
		os.environ['MONO_PATH'] = ':'.join ([
			banshee_path,
			os.path.join (banshee_path, 'Extensions'),
			os.path.join (banshee_path, 'Backends')
		])

		GlickProfile.bundle (self)

		import shutil
		import glob

		for nuke in [ 'AudioCd', 'Dap', 'Dap.MassStorage' ]:
			for path in glob.glob (os.path.join (self.bundle_output_dir,
				'lib', 'banshee-1', 'Extensions', 'Banshee.%s*' % nuke)):
				os.unlink (path)

		for nuke in [ 'gtk20-properties.mo', 'gettext-tools.mo' ]:
			for path in glob.glob (os.path.join (self.bundle_output_dir,
				'share', 'locale', '*', 'LC_MESSAGES', '%s' % nuke)):
				os.unlink (path)

		for nuke in [ 'banshee-1', 'banshee-1/gstreamer-0.10',
				'gdk-pixbuf-2.0/2.10.0/loaders', 'gtk-2.0/2.10.0/engines' ]:
			for path in glob.glob (os.path.join (self.bundle_output_dir,
				'lib', '%s' % nuke, '*.a')):
				os.unlink (path)

if __name__ == '__main__':
	BansheeLinuxBundleProfile ().build ()
