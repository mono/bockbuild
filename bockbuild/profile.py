import os
import build
from util import *
from environment import Environment
from package import *

class Profile:
	def __init__ (self):
		self.name = 'default'
		self.build_root = os.path.join (os.getcwd (), 'build-root')
		self.prefix = os.path.join (self.build_root, '_install')
		self.env = Environment (self)
		self.env.set ('BUILD_PREFIX', self.prefix)
		self.packages = []
		self.cpu_count = get_cpu_count ()
		self.host = get_host ()

	def run (self):
		build.main (self)
	
	def build (self):
		log (0, 'Setting environment variables')
		self.env.compile ()
		self.env.export ()
		for k in self.env.get_names ():
			log (1, '%s = %s' % (k, os.getenv (k)))

		Package.profile = self

		pwd = os.getcwd ()
		for path in self.packages:
			os.chdir (pwd)
			path = os.path.join (os.path.dirname (sys.argv[0]), path)
			exec compile (open (path).read (), path, 'exec')
			if Package.last_instance == None:
				sys.exit ('%s does not provide a valid package.' % path)
			Package.last_instance.start_build ()
			Package.last_instance = None
