class MoblinIconThemePackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'moblin-icon-theme', '2.0.9')
		self.sources = [
			'http://suse-moblin.com/%{name}/%{name}-%{version}.tar.bz2'
		]

		self.bad_prefix = '%{prefix}/_tmp'
		self.icons_dir = '%{prefix}/share/icons'
	
	def build (self):
		self.sh ('autoreconf -fi')
		self.sh ('./configure')
	
	def install (self):
		self.sh ('mkdir -p "%{icons_dir}"')
		self.sh ('rm -rf -- "%{icons_dir}/moblin"')
		self.sh ('LANG=en_US %{makeinstall} DESTDIR="%{bad_prefix}"')
		self.sh ('mv "%{bad_prefix}/usr/local/share/icons/moblin" "%{icons_dir}"')
		self.sh ('rm -rf -- "%{bad_prefix}"')

MoblinIconThemePackage ()
