#!/usr/bin/python -B

import sys
sys.path.append ('../..')

from bockbuild.gnomeprofile import GnomeProfile
from packages import BansheePackages

class BansheeLinuxProfile (GnomeProfile, BansheePackages):
	def __init__ (self):
		GnomeProfile.__init__ (self)
		BansheePackages.__init__ (self)
		self.name = 'linux'

		import os
		if not os.path.isdir ('/usr/include/alsa'):
			raise IOError ('You must have the ALSA headers installed. (/usr/include/alsa)')

if __name__ == '__main__':
	BansheeLinuxProfile ().build ()
