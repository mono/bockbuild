from profile import Profile

class UnixProfile (Profile):
	def __init__ (self, prefix = False):
		Profile.__init__ (self, prefix)
		self.name = 'unix'

		self.gcc_flags = [ '-I%{prefix}/include' ]
		self.ld_flags = [ '-L%{prefix}/lib' ]

		try:
			self.gcc_flags.extend (self.gcc_extra_flags)
		except:
			pass

		try:
			self.ld_flags.extend (self.ld_extra_flags)
		except:
			pass

		self.env.set ('PATH', ':',
			'%{prefix}/bin',
			'/usr/bin',
			'/bin',
			'/usr/local/git/bin')

		self.env.set ('CFLAGS',          '%{gcc_flags}')
		self.env.set ('CXXFLAGS',        '%{env.CFLAGS}')
		self.env.set ('CPPFLAGS',        '%{env.CFLAGS}')
		self.env.set ('C_INCLUDE_PATH',  '%{prefix}/include')

		self.env.set ('LD_LIBRARY_PATH', '%{prefix}/lib')
		self.env.set ('LDFLAGS',         '%{ld_flags}')

		self.env.set ('ACLOCAL_FLAGS',   '-I%{prefix}/share/aclocal')
		self.env.set ('PKG_CONFIG_PATH', ':',
			'%{prefix}/lib/pkgconfig',
			'%{prefix}/share/pkgconfig')

		self.env.set ('XDG_CONFIG_DIRS', '%{prefix}/etc/xdg')
		self.env.set ('XDG_DATA_DIRS',   '%{prefix}/share')
		self.env.set ('XDG_CONFIG_HOME', '$HOME/.config')
