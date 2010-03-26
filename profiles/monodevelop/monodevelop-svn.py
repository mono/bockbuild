class MonoDevelopSvnPackage (Package):
	def __init__ (self):
		Package.__init__ (self, 'monodevelop', 'trunk')

	def svn_co_or_up (self):
		self.cd ('..')
		if os.path.isdir ('svn'):
			self.cd ('svn')
			self.sh ('svn up')
		else:
			self.sh ('svn co http://anonsvn.mono-project.com/source/trunk/monodevelop svn')
			self.cd ('svn')
		self.cd ('..')

	def prep (self):
		self.svn_co_or_up ()
		self.sh ('cp -r svn _build')
		self.cd ('_build/svn')

	def build (self):
		self.sh (
			'echo "main --disable-update-mimedb --disable-update-desktopdb --disable-gnomeplatform --enable-macplatform --disable-tests" > profiles/mac',
			'./configure --prefix="%{prefix}" --profile=mac',
			'make'
		)

	def install (self):
		self.sh ('%{makeinstall}')

MonoDevelopSvnPackage ()
