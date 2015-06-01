import os
from optparse import OptionParser
from util.util import *
from util.csproj import *
from environment import Environment
from package import *

class Profile:
	def __init__ (self, prefix = False):
		self.name = 'default'
		self.root = os.getcwd ()
		self.resource_root = os.path.realpath (os.path.join('..', '..', 'packages'))
		self.build_root = os.path.join (self.root, 'build-root')
		self.stage_root = os.path.join (self.root, 'stage-root')		
		self.toolchain_root = os.path.join (self.root, 'toolchain-root')
		self.prefix = prefix if prefix else os.path.join (self.root, 'install-root')
		self.staged_prefix = os.path.join (self.stage_root, self.prefix [1:])
                self.source_cache = os.getenv('BOCKBUILD_SOURCE_CACHE') or os.path.realpath (os.path.join (self.root, 'cache'))
                self.cpu_count = get_cpu_count ()
		self.host = get_host ()
		self.uname = backtick ('uname -a')

		self.env = Environment (self)
		self.env.set ('BUILD_PREFIX', self.prefix)
		self.env.set ('BOCKBUILD_ENV', '1')
		self.packages = []

		self.find_git ()

		self.bockbuild_revision = backtick (expand_macros ('%{git} rev-parse HEAD', self))[0]

		print 'bockbuild rev.', self.bockbuild_revision
		print '---'

		self.parse_options ()

		packages_to_build = self.cmd_args
		self.verbose = self.cmd_options.verbose
		self.run_phases = self.default_run_phases
		self.arch = self.cmd_options.arch

	def find_git(self):
	        self.git = 'git'
	        for git in ['/usr/local/bin/git', '/usr/local/git/bin/git', '/usr/bin/git']:
				if os.path.isfile (git):
					self.git = git
					break

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
		parser.add_option ('', '--csproj-env', default = False,
			action = 'store_true', dest = 'dump_environment_csproj',
			help = 'Dump the profile environment xml formarted for use in .csproj files')
		parser.add_option ('', '--csproj-insert', default = None,
			action = 'store', dest = 'csproj_file',
			help = 'Inserts the profile environment variables into VS/MonoDevelop .csproj files')
		parser.add_option ('', '--arch', default = 'default',
			action = 'store', dest = 'arch',
			help = 'Select the target architecture(s) for the package')

		self.parser = parser
		self.cmd_options, self.cmd_args = parser.parse_args ()

	def make_package (self, output_dir):
		sys.exit ("Package support not implemented for this profile")

	def bundle (self, output_dir):
		sys.exit ('Bundle support not implemented for this profile')

	def build (self):
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

		if not self.cmd_options.do_build and \
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

		log (0, 'Loaded profile \'%s\' (arch: %s)' % (self.name, self.arch))
		log (0, 'Setting environment variables')

		full_rebuild = False
		tracked_env = []
		tracked_env.extend (dump (self, 'profile'))
		tracked_env.extend (dump (self.cmd_options, 'options'))
		tracked_env.extend (self.env.serialize ())

		env_diff = update (tracked_env, os.path.join (self.root, 'global.env'))

		if env_diff != None:
			full_rebuild = True
			warn ('Environment/configuration changed. Full rebuild triggered')
			warn ('Changes:')
			for line in env_diff:
				print '\t' + line,

		self.env.compile ()
		self.env.export ()

		self.envfile = os.path.join (self.root, self.__class__.__name__) + '_env.sh'
		self.env.dump (self.envfile)
		os.chmod (self.envfile, 0755)
		print 'Environment file: ./%s' % os.path.basename (self.envfile)

		Package.profile = self
		self.toolchain_packages = []
		self.release_packages = []

		for path in self.packages:
			Package.last_instance = None
			exec compile (open (path).read (), path, 'exec')
			if Package.last_instance == None:
				sys.exit ('%s does not provide a valid package.' % path)

			new_package = Package.last_instance
			new_package._path = path
			if new_package.build_dependency:
				self.toolchain_packages.append (new_package)
			else:
				self.release_packages.append (new_package)

		if self.cmd_options.do_build:
			self.ensure_dir (self.source_cache, False)
			self.ensure_dir (self.build_root, full_rebuild)
			self.ensure_dir (self.stage_root, True)
			self.ensure_dir (self.toolchain_root, True)

			print '\n** Building toolchain\n'
			for pkg in self.toolchain_packages:
				pkg.start_build (self.toolchain_root, self.toolchain_root, 'darwin-64') #start_build (workspace, install_root, stage_root)

			print '\n** Building release\n'
			for pkg in self.release_packages:
				pkg.start_build (self.prefix, self.stage_root, self.arch )

		if self.cmd_options.do_bundle:
			if not self.cmd_options.output_dir == None:
				self.bundle_output_dir = os.path.join (os.getcwd (), 'bundle')
			if not self.cmd_options.skeleton_dir == None:
				self.bundle_skeleton_dir = os.path.join (os.getcwd (), 'skeleton')
			self.bundle ()
			return

		if self.cmd_options.do_package:
			self.package ()

	def ensure_dir (self, d, purge):
		if os.path.exists(d):
			if purge:
				log(0, "Purging " + d)
				shutil.rmtree(d, ignore_errors=False)
			else: return
		os.makedirs (d, 0755)

class Bockbuild:
	def main ():
		profile.prep_options ()
		profile.build ()
		profile.package ()


