import os
from optparse import OptionParser
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

	def bundle (self, output_dir):
		sys.exit ('Bundle support not implemented for this profile')

	def build (self):
		default_run_phases = ['prep', 'build', 'install']

		parser = OptionParser (usage = 'usage: %prog [options] [package_names...]')
		parser.add_option ('-b', '--build',
			action = 'store_true', dest = 'do_build', default = False,
			help = 'build the profile')
		parser.add_option ('-z', '--bundle',
			action = 'store_true', dest = 'do_bundle', default = False,
			help = 'create a distributable bundle from a build')
		parser.add_option ('-o', '--output-dir',
			default = None, action = 'store', dest = 'output_dir',
			help = 'output directory for housing the bundle (--bundle|-z)')
		parser.add_option ('-k', '--skeleton-dir',
			default = None, action = 'store',  dest = 'skeleton_dir',
			help = 'skeleton directory containing misc files to copy into bundle (--bundle|-z)')
		parser.add_option ('-v', '--verbose',
			action = 'store_true', dest = 'verbose', default = False,
			help = 'show all build output (e.g. configure, make)')
		parser.add_option ('-i', '--include-phase',
			action = 'append', dest = 'include_run_phases', default = [],
			help = 'explicitly include a build phase to run %s' % default_run_phases)
		parser.add_option ('-x', '--exclude-phase',
			action = 'append', dest = 'exclude_run_phases', default = [],
			help = 'explicitly exclude a build phase from running %s' % default_run_phases)
		parser.add_option ('-s', '--only-sources',
			action = 'store_true', dest = 'only_sources', default = False,
			help = 'only fetch sources, do not run any build phases')
		parser.add_option ('-e', '--environment', default = False,
			action = 'store_true', dest = 'dump_environment',
			help = 'Dump the profile environment as a shell-sourceable list of exports ')
		options, args = parser.parse_args ()

		packages_to_build = args
		self.verbose = options.verbose
		self.run_phases = default_run_phases

		if options.dump_environment:
			self.env.compile ()
			self.env.dump ()
			sys.exit (0)

		if not options.do_build and not options.do_bundle:
			parser.print_help ()
			sys.exit (1)

		if not options.include_run_phases == []:
			self.run_phases = options.include_run_phases
		for exclude_phase in options.exclude_run_phases:
			self.run_phases.remove (exclude_phase)
		if options.only_sources:
			self.run_phases = []

		for phase_set in [self.run_phases,
			options.include_run_phases, options.exclude_run_phases]:
			for phase in phase_set:
				if phase not in default_run_phases:
					sys.exit ('Invalid run phase \'%s\'' % phase)

		log (0, 'Loaded profile \'%s\' (%s)' % (self.name, self.host))
		for phase in self.run_phases:
			log (1, 'Phase \'%s\' will run' % phase)

		log (0, 'Setting environment variables')
		self.env.compile ()
		self.env.export ()
		for k in self.env.get_names ():
			log (1, '%s = %s' % (k, os.getenv (k)))

		Package.profile = self

		if options.do_build:
			pwd = os.getcwd ()
			for path in self.packages:
				os.chdir (pwd)
				path = os.path.join (os.path.dirname (sys.argv[0]), path)
				exec compile (open (path).read (), path, 'exec')
				if Package.last_instance == None:
					sys.exit ('%s does not provide a valid package.' % path)
				Package.last_instance._path = path
				Package.last_instance.start_build ()
				Package.last_instance = None

		if options.do_bundle:
			if not options.output_dir == None:
				self.bundle_output_dir = os.path.join (os.getcwd (), 'bundle')
			if not options.skeleton_dir == None:
				self.bundle_skeleton_dir = os.path.join (os.getcwd (), 'skeleton')
			self.bundle ()
			return
