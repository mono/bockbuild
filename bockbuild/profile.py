import os
from optparse import OptionParser
from util.util import *
from util.csproj import *
from environment import Environment
from package import *

class Profile:
	def __init__ (self, prefix = False):
		self.name = 'default'
		self.build_root = os.path.join (os.getcwd (), 'build-root')
		self.prefix = prefix if prefix else os.path.join (self.build_root, '_install')
		self.env = Environment (self)
		self.env.set ('BUILD_PREFIX', self.prefix)
		self.env.set ('BOCKBUILD_ENV', '1')
		self.packages = []
		self.cpu_count = get_cpu_count ()
		self.global_configure_flags = []
		self.host = get_host ()

		self.parse_options ()

	def parse_options (self):
		self.default_run_phases = ['prep', 'build', 'install']
		parser = OptionParser (usage = 'usage: %prog [options] [package_names...]')
		parser.add_option ('-b', '--build',
			action = 'store_true', dest = 'do_build', default = False,
			help = 'build the profile')
		parser.add_option ('-P', '--package',
			action = 'store_true', dest = 'do_package', default = False,
			help = 'package the profile')
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
			help = 'explicitly include a build phase to run %s' % self.default_run_phases)
		parser.add_option ('-x', '--exclude-phase',
			action = 'append', dest = 'exclude_run_phases', default = [],
			help = 'explicitly exclude a build phase from running %s' % self.default_run_phases)
		parser.add_option ('-s', '--only-sources',
			action = 'store_true', dest = 'only_sources', default = False,
			help = 'only fetch sources, do not run any build phases')
		parser.add_option ('-d', '--debug', default = False,
			action = 'store_true', dest = 'debug',
			help = 'Build with debug flags enabled')
		parser.add_option ('-e', '--environment', default = False,
			action = 'store_true', dest = 'dump_environment',
			help = 'Dump the profile environment as a shell-sourceable list of exports ')
		parser.add_option ('-r', '--release', default = False,
			action = 'store_true', dest = 'release_build',
			help = 'Whether or not this build is a release build')
		parser.add_option ('-p', '--show-source-paths', default = False,
			action = 'store_true', dest = 'show_source_paths',
			help = 'Output a list of all source paths/URLs for all packages')
		parser.add_option ('', '--csproj-env', default = False,
			action = 'store_true', dest = 'dump_environment_csproj',
			help = 'Dump the profile environment xml formarted for use in .csproj files')
		parser.add_option ('', '--csproj-insert', default = None,
			action = 'store', dest = 'csproj_file',
			help = 'Inserts the profile environment variables into VS/MonoDevelop .csproj files')

		self.parser = parser
		self.cmd_options, self.cmd_args = parser.parse_args ()

	def make_package (self, output_dir):
		sys.exit ("Package support not implemented for this profile")

	def bundle (self, output_dir):
		sys.exit ('Bundle support not implemented for this profile')

	def build (self):
		packages_to_build = self.cmd_args
		self.verbose = self.cmd_options.verbose
		self.run_phases = self.default_run_phases

		if self.cmd_options.dump_environment:
			self.env.compile ()
			self.env.dump ()
			sys.exit (0)

		if self.cmd_options.dump_environment_csproj:
			# specify to use our GAC, else MonoDevelop would
			# use its own 
			self.env.set ('MONO_GAC_PREFIX', self.prefix)

			self.env.compile ()
			self.env.dump_csproj ()
			sys.exit (0)

		if self.cmd_options.csproj_file is not None:
			self.env.set ('MONO_GAC_PREFIX', self.prefix)
			self.env.compile ()
			self.env.write_csproj (self.cmd_options.csproj_file)
			sys.exit (0)

		if not self.cmd_options.show_source_paths and \
			not self.cmd_options.do_build and \
			not self.cmd_options.do_bundle and \
			not self.cmd_options.do_package:
			self.parser.print_help ()
			sys.exit (1)

		if not self.cmd_options.include_run_phases == []:
			self.run_phases = self.cmd_options.include_run_phases
		for exclude_phase in self.cmd_options.exclude_run_phases:
			self.run_phases.remove (exclude_phase)
		if self.cmd_options.only_sources:
			self.run_phases = []

		for phase_set in [self.run_phases,
			self.cmd_options.include_run_phases, self.cmd_options.exclude_run_phases]:
			for phase in phase_set:
				if phase not in self.default_run_phases:
					sys.exit ('Invalid run phase \'%s\'' % phase)

		log (0, 'Loaded profile \'%s\' (%s)' % (self.name, self.host))
		for phase in self.run_phases:
			log (1, 'Phase \'%s\' will run' % phase)

		log (0, 'Setting environment variables')
		self.env.compile ()
		self.env.export ()
		for k in self.env.get_names ():
			log (1, '%s = %s' % (k, os.getenv (k)))

		source_cache = os.getenv('BOCKBUILD_SOURCE_CACHE')
                source_cache = source_cache or os.path.realpath (os.path.join (self.build_root, "..", "..", "..", "cache"))
		log (1, 'Source cache: %s' % source_cache)

		Package.profile = self

		if self.cmd_options.do_build or self.cmd_options.show_source_paths:
			pwd = os.getcwd ()
			for path in self.packages:
				os.chdir (pwd)
				path = os.path.join (os.path.dirname (sys.argv[0]), path)
				exec compile (open (path).read (), path, 'exec')
				if Package.last_instance == None:
					sys.exit ('%s does not provide a valid package.' % path)
				Package.last_instance._path = path
				if self.cmd_options.do_build:
					Package.last_instance.start_build ()
				else:
					expand_macros (Package.last_instance, Package.last_instance)
					if Package.last_instance.sources:
						for source in Package.last_instance.sources:
							print '%s\t%s\t%s\t%s' % (Package.last_instance.name,
								Package.last_instance.version, os.path.dirname (source),
								os.path.basename (source))

				Package.last_instance = None

		if self.cmd_options.show_source_paths:
			sys.exit (0)

		if self.cmd_options.do_bundle:
			if not self.cmd_options.output_dir == None:
				self.bundle_output_dir = os.path.join (os.getcwd (), 'bundle')
			if not self.cmd_options.skeleton_dir == None:
				self.bundle_skeleton_dir = os.path.join (os.getcwd (), 'skeleton')
			self.bundle ()
			return

		if self.cmd_options.do_package:
			self.package ()
