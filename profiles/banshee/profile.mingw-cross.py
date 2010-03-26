#!/usr/bin/python -B

import os
import sys

sys.path.append ('../..')

from bockbuild.unixprofile import UnixProfile
from packages import BansheePackages

class BansheeMingwCrossProfile (UnixProfile, BansheePackages):
	def __init__ (self):
		UnixProfile.__init__ (self)
		BansheePackages.__init__ (self)
		self.build_root = os.path.join (os.getcwd (), 'build-root-mingw')
		
		self.name = 'mingw-cross'

		self.host = 'i686-linux'
		self.target = 'i686-pc-mingw32'
		self.sysroot = '/usr/%{target}/sys-root/%{target}'
		
		self.global_configure_flags.extend ([
			"--host=%s" % self.host,
			"--target=%s" % self.target
		])

		self.gcc_flags.extend ([
			'-I%{sysroot}/include',
			'-m32',
			'-march=i586',
			'-mms-bitfields'
		])

		self.env.set ('PATH', ':',
			'%{prefix}/bin',
			'%{sysroot}/bin',
			'/usr/bin',
			'/bin')

		self.ld_flags.extend ([
			'-L%{sysroot}/lib',
			'-m32'
		])

		self.env.set ('CC', '%{target}-gcc')
		self.env.set ('CXX', '%{target}-g++')

BansheeMingwCrossProfile ().build ()
