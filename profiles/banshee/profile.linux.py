#!/usr/bin/python -B

import sys
sys.path.append ('../..')

from bockbuild.unixprofile import UnixProfile
from packages import BansheePackages

class BansheeLinuxProfile (UnixProfile, BansheePackages):
	def __init__ (self):
		UnixProfile.__init__ (self)
		BansheePackages.__init__ (self)
		self.name = 'linux'

		import os
		if not os.path.isdir ('/usr/include/alsa'):
			raise IOError ('You must have the ALSA headers installed. (/usr/include/alsa)')

BansheeLinuxProfile ().build ()
