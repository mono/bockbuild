#!/usr/bin/python -B

from linux import BansheeLinuxProfile

class BansheeMeeGoProfile (BansheeLinuxProfile):
	def __init__ (self):
		self.gcc_extra_flags = [
			'-O2',
			'-g',
			'-pipe',
			'-Wall',
			'-Wp,-D_FORTIFY_SOURCE=2',
			'-fexceptions',
			'-fstack-protector',
			'--param=ssp-buffer-size=4',
			'-Wformat',
			'-Wformat-security'
		]

		self.gcc_extra_flags_i686 = [
			'-m32',
			'-march=core2',
			'-mssse3',
			'-mtune=atom',
			'-mfpmath=sse',
			'-fasynchronous-unwind-tables',
			'-fno-omit-frame-pointer'
		]

		self.gcc_extra_flags.extend (self.gcc_extra_flags_i686)
		
		BansheeLinuxProfile.__init__ (self)
		self.name = 'meego'

BansheeMeeGoProfile ().build ()
