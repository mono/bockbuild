
class MonoBasicPackage (GitHubTarballPackage):
	def __init__ (self):
		GitHubTarballPackage.__init__ (self, 'mono', 'mono-basic', '4.0.1', 'b8011b2f274606323da0927214ed98336465f467',
				configure = './configure --prefix="%{staged_profile}"')

	def install (self):
		self.sh ('./configure --prefix="%{staged_prefix}"')
		self.sh ('make install')

MonoBasicPackage()