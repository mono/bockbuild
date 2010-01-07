import os
from unixprofile import UnixProfile

class DarwinProfile (UnixProfile):
	def __init__ (self):
		UnixProfile.__init__ (self)
		
		self.name = 'darwin'
		self.mac_sdk_path = '/Developer/SDKs/MacOSX10.5.sdk'
		
		if not os.path.isdir (self.mac_sdk_path):
			raise IOError ('Mac OS X SDK does not exist: %s' \
				% self.mac_sdk_path)

		self.gcc_flags.extend ([
			'-D_XOPEN_SOURCE',
			'-isysroot %{mac_sdk_path}',
			'-mmacosx-version-min=10.5'
		])

		self.env.set ('CC',  'gcc-4.2')
		self.env.set ('CXX', 'g++-4.2')
