import os
from optparse import OptionParser
from util.util import *
from util.csproj import *
from environment import Environment
from bockbuild.package import *
import collections
import hashlib
import itertools

class Profile:
	def __init__ (self, prefix = False):
		self.name = 'bockbuild'
		self.root = os.getcwd ()
		self.resource_root = os.path.realpath (os.path.join('..', '..', 'packages'))
		self.build_root = os.path.join (self.root, 'build-root')
		self.staged_prefix = os.path.join (self.root, 'stage-root')
		self.toolchain_root = os.path.join (self.root, 'toolchain-root')
		self.artifact_root = os.path.join (self.root, 'artifacts')
		self.package_root = os.path.join (self.root, 'package-root')
		self.scratch = os.path.join (self.root, 'scratch')
		self.logs = os.path.join (self.root, 'logs')
		self.env_file = os.path.join (self.root, 'global.env')
		self.source_cache = os.getenv('BOCKBUILD_SOURCE_CACHE') or os.path.realpath (os.path.join (self.root, 'cache'))
		self.cpu_count = get_cpu_count ()
		self.host = get_host ()
		self.uname = backtick ('uname -a')

		self.env = Environment (self)
		self.env.set ('BUILD_PREFIX', '%{prefix}')
		self.env.set ('BUILD_ARCH', '%{arch}')
		self.env.set ('BOCKBUILD_ENV', '1')

		self.env.set ('bockbuild_buildver', '1')

		self.full_rebuild = False

		self.profile_name = self.__class__.__name__

		find_git (self)
		self.bockbuild_rev =  git_get_revision(self, self.root)

		loginit ('bockbuild (%s)' % (git_shortid (self, self.root)))
		info ('cmd: %s' % ' '.join(sys.argv))

		self.parse_options ()
		self.toolchain = []
		self.packages_to_build = self.cmd_args or self.packages
		self.verbose = self.cmd_options.verbose
		config.verbose = self.cmd_options.verbose
		self.arch = self.cmd_options.arch
		self.unsafe = self.cmd_options.unsafe
		config.trace = self.cmd_options.trace
		self.tracked_env = []

		Package.profile = self

		ensure_dir (self.source_cache, purge = False)
		ensure_dir (self.artifact_root, purge = False)
		ensure_dir (self.build_root, purge = False)
		ensure_dir (self.scratch, purge = True)
		ensure_dir (self.logs, purge = False)

	def parse_options (self):
		parser = OptionParser (usage = 'usage: %prog [options] [package_names...]')
		parser.add_option ('-b', '--build',
			action = 'store_true', dest = 'do_build', default = False,
			help = 'build the profile')
		parser.add_option ('-P', '--package',
			action = 'store_true', dest = 'do_package', default = False,
			help = 'package the profile')
		parser.add_option ('-v', '--verbose',
			action = 'store_true', dest = 'verbose', default = False,
			help = 'show all build output (e.g. configure, make)')
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
		parser.add_option ('', '--shell', default = False,
			action = 'store_true', dest = 'shell',
			help = 'Get an shell with the package environment')
		parser.add_option ('', '--unsafe', default = False,
			action = 'store_true', dest = 'unsafe',
			help = 'Prevents full rebuilds when a build environment change is detected. Useful for debugging.')
		parser.add_option ('', '--trace', default = False,
			action = 'store_true', dest = 'trace',
			help = 'Enable tracing (for diagnosing bockbuild problems')

		self.parser = parser
		self.cmd_options, self.cmd_args = parser.parse_args ()

	def make_package (self, output_dir):
		sys.exit ("Package support not implemented for this profile")

	def bundle (self, output_dir):
		sys.exit ('Bundle support not implemented for this profile')

	def build_distribution (self, packages, dest, stage):
		#TODO: full relocation means that we shouldn't need dest at this stage
		build_list = []

		progress ('Fetching packages')
		for package in packages.values ():
			package.build_artifact = os.path.join (self.artifact_root, package.name)
			package.buildstring_file = package.build_artifact + '.buildstring'
			package.log = os.path.join (self.logs, package.name + '.log')
			if os.path.exists (package.log):
				delete (package.log)

			retry (package.fetch)

			if self.full_rebuild:
				package.request_build ('Full rebuild')

			elif not os.path.exists (package.build_artifact):
				package.request_build ('No artifact')

			elif is_changed (package.buildstring, package.buildstring_file):
				package.request_build ('Updated')

			if package.needs_build:
				build_list.append (package)

		verbose ('%d packages need building:' % len (build_list))
		verbose (['%s (%s)' % (x.name, x.needs_build) for x in build_list])

		for package in packages.values ():
			package.start_build (self.arch, dest, stage)
			#make artifact in scratch
			#delete artifact + buildstring
			with open (package.buildstring_file, 'w') as output:
				output.write ('\n'.join (package.buildstring))

	def build (self):

		if self.cmd_options.dump_environment:
			self.env.compile ()
			self.env.dump ()
			sys.exit (0)

		if self.cmd_options.dump_environment_csproj:
			# specify to use our GAC, else MonoDevelop would
			# use its own 
			self.env.set ('MONO_GAC_PREFIX', self.staged_prefix)

			self.env.compile ()
			self.env.dump_csproj ()
			sys.exit (0)

		if self.cmd_options.csproj_file is not None:
			self.env.set ('MONO_GAC_PREFIX', self.staged_prefix)
			self.env.compile ()
			self.env.write_csproj (self.cmd_options.csproj_file)
			sys.exit (0)

		self.toolchain_packages = collections.OrderedDict()
		for source in self.toolchain:
			package = self.load_package (source)
			self.toolchain_packages [package.name] = package

		self.setup_toolchain ()

		self.release_packages = collections.OrderedDict()
		for source in self.packages_to_build:
			package = self.load_package (source)
			self.release_packages [package.name] = package

		self.setup_release ()

		if self.track_env ():
			if self.unsafe:
				warn ('Build environment changed, but overriding full rebuild!')
			else:
				info ('Build environment changed, full rebuild triggered')
				self.full_rebuild = True
				ensure_dir (self.build_root, purge = True)

		if self.cmd_options.shell:
			title ('Shell')
			self.shell ()

		if self.cmd_options.do_build:
			ensure_dir (self.toolchain_root, purge = True)
			ensure_dir (self.staged_prefix, purge = True)

			title ('Building toolchain')
			self.build_distribution (self.toolchain_packages, self.toolchain_root, self.toolchain_root)

			title ('Building release')
			self.build_distribution (self.release_packages, self.prefix, self.staged_prefix)

			#update env
			with open (self.env_file, 'w') as output:
				output.write ('\n'.join (self.tracked_env))

		if self.cmd_options.do_package:
			title ('Packaging')
			protect_dir (self.staged_prefix)
			ensure_dir (self.package_root, True)

			run_shell('rsync -aPq %s/* %s' % (self.staged_prefix, self.package_root), False)
			unprotect_dir (self.package_root)

			self.process_release (self.package_root)
			self.package ()

	def track_env (self):
		self.env.compile ()
		self.env.export ()
		self.env_script = os.path.join (self.root, self.profile_name) + '_env.sh'
		self.env.write_source_script (self.env_script)
		
		self.tracked_env.extend (self.env.serialize ())
		return is_changed (self.tracked_env, self.env_file)

	def load_package (self, source):
		if isinstance (source, Package): # package can already be loaded in the source list
			return source

		if not os.path.isabs (source):
			fullpath = os.path.join (self.resource_root, source + '.py')
		else:
			fullpath = source

		if not os.path.exists (fullpath):
			error ("Resource '%s' not found" % source)

		Package.last_instance = None

		execfile (fullpath, globals())

		if Package.last_instance == None:
			error ('%s does not provide a valid package.' % source)

		new_package = Package.last_instance
		new_package._path = fullpath
		return new_package

	class FileProcessor (object):
		def __init__ (self, harness = None, match = None, process = None,  extra_files = None):
			self.harness = harness
			self.match = match
			self.files = list (extra_files) if extra_files else list ()
			self.root = None

		def relpath (self, path):
			return os.path.relpath (path, self.root)

		def run (self):
			for path in self.files:
				self.harness (path, self.process)
		def end (self):
			return


	def postprocess (self, processors, directory, filefilter = None):
		def simple_harness (path, func):
			if not os.path.lexists (path):
				return # file removed by previous processor function
			# TODO: Fix so that it works on symlinks
			# hash = hashlib.sha1(open(path).read()).hexdigest()
			func (path)
			if not os.path.lexists (path):
				trace ('Removed file: %s' % path)
			#if hash != hashlib.sha1(open(path).read()).hexdigest():
			#	warn ('Changed file: %s' % path)

		for proc in processors:
			proc.root = directory
			if proc.harness == None:
				proc.harness = simple_harness
			if proc.match == None:
					error ('proc %s has no match function' % proc.__class__.__name__)

		for path in filter (filefilter, iterate_dir (directory, with_dirs = True, with_links = True)):
			filetype = get_filetype (path)
			for proc in processors:
				if proc.match (path, filetype) == True:
					trace ('%s  matched %s / %s' % (proc.__class__.__name__, os.path.basename(path), filetype) )
					proc.files.append (path)

		for proc in processors:
			verbose ('%s: %s items' % (proc.__class__.__name__ , len (proc.files)))
			proc.run ()


		for proc in processors:
			proc.end ()
			proc.harness = None
			proc.files = []

