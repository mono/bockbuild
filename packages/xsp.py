class XspPackage (GitHubTarballPackage):
	def __init__ (self):
		GitHubTarballPackage.__init__ (self, 'mono', 'xsp', '3.0.11',
			'e272a2c006211b6b03be2ef5bbb9e3f8fefd0768',
			 configure = './autogen.sh --prefix="%{package_prefix}"')

	def install (self):
		# scoop up some mislocated files
		misdir = '%s%s' % (self.stage_root, self.staged_profile)
		unprotect_dir (self.stage_root)
		Package.install (self)
		if not os.path.exists (misdir):
			for path in iterate_dir (self.stage_root):
				print path
			error ('Could not find mislocated files')

		self.sh('rsync -a --ignore-existing %s/* %s' % (misdir, self.profile.staged_prefix))
		self.sh('rm -rf %s/*' % misdir)


XspPackage ()
