import os

class BooPackage (Package):
	def __init__(self):
		Package.__init__ (self, 'boo', '0.9.4.9', sources = ['http://dist.codehaus.org/boo/distributions/boo-0.9.4.9.tar.gz'])

	def install(self):
		# Unfortunately boo's build scripts don't seem to do a very good job 
		for script in [ 'booc', 'booi', 'booish' ]:
			replace_in_file (os.path.join ('extras', script), { '${exec_prefix}': self.prefix })
		self.sh ('make install MIME_PREFIX=/tmp GTKSOURCEVIEW_PREFIX=/tmp')

BooPackage ()
