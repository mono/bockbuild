#!/usr/bin/python -B

import os
import sys

sys.path.append ('../..')

from bockbuild.darwinprofile import DarwinProfile
from packages import MonoDevelopPackages

class MonoDevelopDarwinProfile (DarwinProfile, MonoDevelopPackages):
	def __init__ (self):
		DarwinProfile.__init__ (self)
		MonoDevelopPackages.__init__ (self)

		self_dir = os.path.realpath (os.path.dirname (sys.argv[0]))
		self.bundle_skeleton_dir = os.path.join (self_dir, 'skeleton.darwin')
		self.bundle_output_dir = os.path.join (self_dir, 'bundle.darwin')

		self.bundle_from_build = [
			'bin/mono',
			'lib/mono/2.0/gmcs.exe',
			'lib/mono/gac/Mono.Addins.CecilReflector',
			'lib/monodevelop',
			'lib/pango',
			'lib/gtk-2.0/2.10.0/loaders',
			'lib/gtk-2.0/2.10.0/engines',
			'lib/gtk-2.0/2.10.0/immodules',
			'share/monodevelop',
			'share/locale',
			'etc/mono/config',
			'etc/mono/1.0/machine.config',
			'etc/mono/2.0/machine.config',
			'etc/mono/2.0/settings.map',
			'share/icons/hicolor/index.theme',
			'share/icons/Tango/index.theme'
		]

		self.bundle_from_build.extend ([
			'share/icons/%s/%sx%s' % (theme, size, size)
				for size in [16, 22, 32, 48]
				for theme in ['hicolor', 'Tango']
		])

MonoDevelopDarwinProfile ().build ()
