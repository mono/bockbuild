
class MonoBasicPackage (GitHubTarballPackage):
	def __init__ (self):
		GitHubTarballPackage.__init__ (self, 'mono', 'mono-basic', '4.4', '8a804fd8f12f2e6a002173bbbc0974197530ec2f',
				configure = './configure --prefix="%{staged_profile}"')

	def install (self):
		self.sh ('./configure --prefix="%{staged_prefix}"')
		self.sh ('make install')

MonoBasicPackage()