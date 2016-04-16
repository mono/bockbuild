class MSBuild (GitHubPackage):
	def __init__ (self):
		GitHubPackage.__init__ (self, 'mono', 'msbuild', '14.1',
			git_branch = 'xplat-p1')

	def build (self):
		self.sh ('./cibuild.sh --scope Compile --target Mono --host Mono')

	def install (self):
		# adjusted from 'install-mono-prefix.sh'

		build_output = 'bin/Debug-MONO/OSX_Deployment'
		new_location = os.path.join (self.staged_prefix, 'lib/mono/msbuild/%s/bin' % self.version)
		bindir = os.path.join (self.staged_prefix, 'bin')

		os.makedirs(new_location)
		self.sh('cp -R %s/* %s' % (build_output, new_location))

		os.makedirs(bindir)
		self.sh('cp msbuild-mono-deploy.in %s/msbuild' % bindir)

		for excluded in glob.glob("%s/*UnitTests*" % new_location):
			self.rm(excluded)

		for excluded in glob.glob("%s/*xunit*" % new_location):
			self.rm(excluded)

MSBuild ()