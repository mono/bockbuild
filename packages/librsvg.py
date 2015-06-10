class LibrsvgPackage(GnomeXzPackage):
	def __init__ (self):
		GnomeXzPackage.__init__(self, 'librsvg', version_major = '2.37', version_minor = '0',
        configure_flags = [ '--disable-Bsymbolic', '--disable-introspection' ])

	def install (self):
		Package.install (self)
		# scoop up some mislocated files 
		run_shell('rsync -a --ignore-existing %s/%s/* %s' % (self.profile.stage_root, self.profile.staged_prefix, self.profile.staged_prefix), True)
		run_shell('rm -rf %s/%s/*' % (self.profile.stage_root, self.profile.staged_prefix), True)

LibrsvgPackage()
