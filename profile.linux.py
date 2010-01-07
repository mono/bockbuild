#!/usr/bin/env python -B

from bockbuild.unixprofile import UnixProfile
from packages import BansheePackages

class BansheeLinuxProfile (UnixProfile, BansheePackages):
	def __init__ (self):
		UnixProfile.__init__ (self)
		BansheePackages.__init__ (self)

		import os
		if not os.path.isdir ('/usr/include/alsa'):
			raise IOError ('You must have the ALSA headers installed. (/usr/include/alsa)')

BansheeLinuxProfile ().run ()
