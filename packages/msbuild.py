import fileinput

class MSBuild (GitHubPackage):
	def __init__ (self):
		GitHubPackage.__init__ (self, 'xamarin', 'msbuild', '15.0',
			git_branch = 'd15.3')

	def build (self):
		self.sh ('./cibuild.sh --scope Compile --target Mono --host Mono --config Release')

	def install (self):
                self.sh ('./install-mono-prefix.sh %s' % self.staged_prefix)

MSBuild ()
