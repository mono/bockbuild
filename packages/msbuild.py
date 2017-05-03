import fileinput

class MSBuild (Package):
	def __init__ (self):
		Package.__init__ (self, 'msbuild', '15.0',
                        organization = 'mono',
                        sources = ['git@github.com:xamarin/msbuild.git'],
			git_branch = 'd15.3')

	def build (self):
		self.sh ('./cibuild.sh --scope Compile --target Mono --host Mono --config Release')

	def install (self):
                self.sh ('./install-mono-prefix.sh %s' % self.staged_prefix)

MSBuild ()
