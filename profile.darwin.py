#!/usr/bin/env python -B

from bockbuild.darwinprofile import DarwinProfile
from packages import BansheePackages

class BansheeDarwinProfile (DarwinProfile, BansheePackages):
	def __init__ (self):
		DarwinProfile.__init__ (self)
		BansheePackages.__init__ (self)

BansheeDarwinProfile ().build ()
