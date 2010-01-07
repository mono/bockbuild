class GtkSharpPackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'gtk-sharp', '2-12-branch')
		self.branch = '212'
		# self.sources = [
		# 	'http://ftp.novell.com/pub/mono/sources/%{name}%{branch}/%{name}-%{version}.tar.bz2'
		# ]

	def svn_co_or_up (self):
		self.cd ('..')
		if os.path.isdir ('svn'):
			self.cd ('svn')
			#self.sh ('svn up')
		else:
			self.sh ('svn co http://anonsvn.mono-project.com/source/branches/%{name}-%{version} svn')
			self.cd ('svn')
		self.cd ('..')

	def prep (self):
		self.svn_co_or_up ()
		self.sh ('cp -r svn _build')
		self.cd ('_build/svn')

	def build (self):
		self.sh (
			'./bootstrap-2.12 --prefix="%{prefix}"',
			'%{make}'
		)

	def install (self):
		self.sh ('%{makeinstall}')

GtkSharpPackage ()
