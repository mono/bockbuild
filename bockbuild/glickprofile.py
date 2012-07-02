import os
import shutil
from plistlib import Plist
from util.util import *
from unixprofile import UnixProfile

class GlickProfile (UnixProfile):
	def __init__ (self):
		UnixProfile.__init__ (self)
		
		self.name = 'glick'
		self.prefix = '/proc/self/fd/1023'
		self.env.set ('BUILD_PREFIX', self.prefix)
		
		self.glick_path = '/usr/bin/mkglick'
		
		if not os.path.exists (self.glick_path):
			raise IOError ('Glick is not installed (http://www.gnome.org/~alexl/glick/): %s' \
				% self.glick_path)

		if not os.path.exists (self.prefix):
			raise IOError ('We are not running in a glick magic shell')

	def bundle (self):
		self.make_app_bundle ()

	def make_app_bundle (self):
		start_path = os.path.join (self.bundle_skeleton_dir, 'start')
		if not os.path.exists (start_path):
			print 'Warning: no start script in glick skeleton'

		# Create the bundle, copying the skeleton
		shutil.rmtree (self.bundle_output_dir, ignore_errors = True)
		shutil.copytree (self.bundle_skeleton_dir, self.bundle_output_dir)

		# Run solitary against the installation to collect files
		files = ''
		for file in self.bundle_from_build:
			files = files + ' "%s"' % os.path.join (self.prefix, file)

		run_shell ('mono --debug ../../solitary/Solitary.exe '
			'--mono-prefix="%s" --root="%s" --out="%s" %s' % \
			(self.prefix, self.prefix, self.bundle_output_dir, files))

