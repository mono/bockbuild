#!/usr/bin/python -B

import os
import sys

from bockbuild.darwinprofile import DarwinProfile
from packages import BansheePackages

class BansheeDarwinProfile (DarwinProfile, BansheePackages):
	def __init__ (self):
		DarwinProfile.__init__ (self)
		BansheePackages.__init__ (self)

		self_dir = os.path.realpath (os.path.dirname (sys.argv[0]))
		self.bundle_skeleton_dir = os.path.join (self_dir, 'skeleton.darwin')
		self.bundle_output_dir = os.path.join (self_dir, 'bundle.darwin')

		self.bundle_from_build = [
			'bin/mono',
			'bin/banshee-1',
			'bin/pango-querymodules',
			'bin/gtk-demo',
			'lib/banshee-1',
			'lib/pango',
			'lib/gstreamer-0.10',
			'share/banshee-1',
			'etc/mono/config',
			'etc/mono/1.0/machine.config',
			'etc/mono/2.0/machine.config',
			'etc/mono/2.0/settings.map'
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

		DarwinProfile.bundle (self)
		self.configure_pango ()

		import shutil
		import glob

		bin_path = os.path.join (self.bundle_macos_dir, 'Banshee')
		shutil.move (os.path.join (self.bundle_res_dir, 'bin', 'banshee-1'), bin_path)
		os.chmod (bin_path, 0755)

		for nuke in [ 'NotificationArea', 'AudioCd', 'Dap',
			'Dap.MassStorage', 'MiniMode' ]:
			for path in glob.glob (os.path.join (self.bundle_res_dir,
				'lib', 'banshee-1', 'Extensions', 'Banshee.%s*' % nuke)):
				os.unlink (path)

BansheeDarwinProfile ().build ()
