import hashlib
import os
import sys
import shutil
import tempfile
import filecmp
import datetime
import stat
import time
from urllib import FancyURLopener
from util.util import *

class Package:
	def __init__ (self, name, version = None, organization = None, configure_flags = None, sources = None, revision = None, git_branch = None, source_dir_name = None, override_properties = None, configure = None):
		Package.last_instance = self

		self.verbose = False

		self.name = name
		self.version = version
		self.organization = organization

		self.configure_flags = []
		self.gcc_flags = list(Package.profile.gcc_flags)
		self.cpp_flags = list(Package.profile.gcc_flags)
		self.ld_flags = list(Package.profile.ld_flags)

		self.local_cpp_flags = []
		self.local_gcc_flags = []
		self.local_ld_flags = []
		self.local_configure_flags = []

		self.build_env = ''
		self.desc = None
		self.buildstring = None

		self._dirstack = []

		# additional files that need staging (besides binaries and scripts)
		# (use path relative to prefix root e.g. 'etc/something.config')
		self.extra_stage_files = []

		# fat binary parameters. On a 64-bit Darwin profile (m64 = True) 
		# each package must decide if it will a) perform a multi-arch (64/32) build 
		# b) request two builds that are lipoed at the end or c) request a 32-bit
		# build only.

		self.needs_lipo = False
		self.m32_only = False
		self.build_dependency = False
		self.dont_clean = False
		self.needs_build = False

		if configure_flags:
			self.configure_flags.extend (configure_flags)

		self.sources = sources
		if self.sources == None \
			and not self.__class__.default_sources == None:
			self.sources = list (self.__class__.default_sources)

		if self.organization == None and self.sources != None and len(self.sources) > 0:
			self.organization = self.extract_organization (self.sources[0])

		self.source_dir_name = source_dir_name
		if self.source_dir_name == None:
			self.source_dir_name = "%s-%s" % (name, version)

		self.revision = revision

		if configure:
			self.configure = configure
		else:
			self.configure = './configure --prefix="%{package_prefix}"'

		self.make = 'make -j%s' % Package.profile.cpu_count
		self.makeinstall = None
		
		self.git = 'git'
		self.git_branch = git_branch
		for git in ['/usr/local/bin/git', '/usr/local/git/bin/git', '/usr/bin/git']:
			if os.path.isfile (git):
				self.git = git
				break

		if not override_properties == None:
			for k, v in override_properties.iteritems ():
				self.__dict__[k] = v

		self.makeinstall = self.makeinstall or 'make install DESTDIR=%{stage_root}'

	def extract_organization (self, source):
		if (not "git" in source) or ("http" in source):
			return None
		if "git.gnome.org" in source:
			return None
		if "github" in source:
			pattern = r"github.com\W(\w+)\/\S+\.git"
			match = re.search(pattern, source)
			if match:
				return match.group(1)
			else:
				raise Exception ("Cannot determine organization for %s" % source)
		else:
			raise Exception ("Cannot determine organization for %s" % source)

	def try_get_version (self, source_dir):
		configure_ac = os.path.join (source_dir, 'configure.ac')
		if os.path.exists (configure_ac):
			with open (configure_ac) as file:
				pattern = r"AC_INIT\(\S+?\s*,\s*\[(\d\S+?)\]" #AC_INIT (...,[VERSION]...
				for x in range (40):
					line = file.readline ()
					match = re.search(pattern, line)
					if match:
						return match.group(1)

	def trace (self, message):
		trace (message, skip = 1)

	def resolve_version (self):
		package_version = expand_macros (self.version, self)
		found_version = self.try_get_version (self.workspace) or package_version
		if package_version == None:
			package_version = found_version
			trace ('%s: Using found version %s' % (self.name, found_version))
		elif found_version[0] != package_version[0]: # major version differs
			warn ('Version in configure.ac is %s, package declares %s' % (found_version, package_version))
		self.version = package_version


	def _fetch_sources (self, build_root, workspace, resource_dir, source_cache_dir):
		trace ('Fetching %s' % workspace)
		clean_func = None # what to run if the workspace needs to be redone

		if self.sources == None:
			return None

		def checkout (self, source_url, cache_dir, workspace_dir):
			def clean_git_workspace ():
				trace ('Cleaning git workspace: ' + self.name)
				self.pushd (workspace_dir)
				try:
					self.sh ('%{git} reset --hard')
					if config.iterative == False:
						self.sh ('%{git} clean -xffd')
					else:
						warn ('iterative')
				finally:
					self.popd ()

			def create_cache ():
				self.cd (build_root)
				# since this is a fresh cache, the workspace copy is invalid if it exists
				if os.path.exists (workspace_dir):
					self.rm (workspace_dir)
				progress ('Cloning git repo: %s' % source_url)
				self.sh ('%' + '{git} clone --mirror "%s" "%s"' % (source_url, cache_dir))

			def update_cache ():
				trace ( 'Updating cache: ' + cache_dir)
				self.cd (cache_dir)
				try:
					if self.git_branch == None:
						self.sh ('%{git} fetch --all --prune')
					else:
						self.sh ('%' + '{git} fetch origin %s' % self.git_branch)
				except Exception as e:
					self.cd (build_root)
					raise

			def create_workspace ():
				self.cd (build_root)
				self.sh ('%' + '{git} clone --local --shared 	"%s" "%s"' % (cache_dir, workspace_dir))

			def update_workspace ():
				trace ( 'Updating workspace')
				self.cd (workspace_dir)

				if self.git_branch == None:
					self.sh ('%{git} fetch --all --prune')
				else:
					self.sh ('%' + '{git} fetch origin %s:refs/remotes/origin/%s' % (self.git_branch, self.git_branch))
				self.cd (build_root)

			def resolve ():
				self.cd (workspace_dir)
				current_revision = git_get_revision (self)

				if current_revision == self.revision:
					return

				if self.revision  == None and self.git_branch == None:
					warn ('Package does not define revision or branch, defaulting to tip of "master"')
					self.git_branch = self.git_branch or 'master'

				if self.revision != None:
					target_revision = self.revision

				if self.git_branch != None:
					self.sh ('%' + '{git} checkout %s' % self.git_branch)
					self.sh ('%' + '{git} merge origin/%s --ff-only ' % self.git_branch)
					current_revision = git_get_revision (self)

					if self.revision == None: # target the tip of the branch
						target_revision = git_get_revision (self)

				if (current_revision != target_revision):
					self.request_build ('Revision changed (%s -> %s)' % (current_revision, target_revision))
					self.sh ('%' + '{git} reset --hard %s' % target_revision)
				self.sh ('%' + '{git} submodule update --recursive')

				current_revision = git_get_revision (self)

				if (self.revision != None and self.revision != current_revision):
					error ('Workspace error: Revision is %s, package specifies %s' % (current_revision, self.revision))

				self.revision = current_revision

			def define ():
				self.resolve_version ()

				str = self.name
				if self.version:
					str+= ' v.' + self.version

				str += ' (%s)' % git_shortid (self)

				self.desc = str
				self.buildstring = ['%s <%s>' % (str, source_url)]

			if os.path.exists (cache_dir):
				update_cache ()
			else:
				create_cache ()

			if os.path.exists (workspace_dir):
				if self.dont_clean == True: # previous workspace was left dirty, delete
					clean_git_workspace ()
				update_workspace ()
			else:
				create_workspace ()

			cache = None # at this point, the cache is not the problem; keep _fetch_sources from deleting it

			resolve ()
			define ()
			self.cd (build_root)
			return clean_git_workspace

		def checkout_archive (archive, cache_dest, workspace_dir):
			def create_cache ():
				if not os.path.exists (cache_dest):
					progress ('Downloading: %s' % archive)
					filename, message = FancyURLopener ().retrieve (archive, cache_dest)

			def update_cache ():
				pass

			def create_workspace ():
				self.extract_archive (cache_dest, False)
				if not os.path.exists (workspace_dir):
					error ('Archive %s was extracted but not found at workspace path %s' % (cache_dest, workspace_dir))

			def update_workspace ():
				pass

			def clean_archive ():
				self.pushd (build_root)
				try:
					self.rm (workspace)
					create_workspace ()
					self.popd ()
				except Exception as e:
					self.rm_if_exists (cache_dest)
					self.rm_if_exists (workspace_dir)
					raise

			def define ():
				self.pushd (workspace_dir)
				self.resolve_version ()
				self.desc = '%s v. %s' % (self.name, self.version)
				self.buildstring = ['%s <%s> md5: %s)' % (self.desc, archive, md5 (cache_dest))]
				self.popd ()

			if os.path.exists (cache_dest):
					update_cache ()
			else:
					create_cache ()

			if os.path.exists (workspace_dir):
				update_workspace ()
			else:
				create_workspace ()

			define ()

			return clean_archive

		def get_download_dest(url):
			return os.path.join (source_cache_dir, os.path.basename (url))

		def get_git_cache_path ():
			if self.organization is None:
				name = self.name
			else:
				name = self.organization + "+" + self.name
			return os.path.join (source_cache_dir, name)

		def is_updated (path):
			trace (path)
			if artifact_stamp is None:
				return
			if os.path.isfile (path) and os.path.getmtime(path) > artifact_stamp:
				self.request_build ('Updated: %s (%s vs %s)' % (path, os.path.getmtime(path), artifact_stamp))
			elif os.path.isdir (path):
				for root, dirs, files in os.walk (path):
					dirs[:] = [d for d in dirs if not d[0] == '.'] # http://stackoverflow.com/questions/13454164/os-walk-without-hidden-folders
					for dir in dirs:
						dir_path = os.path.join (root, dir)
						if os.path.isdir(dir_path) and os.path.getmtime(dir_path) > artifact_stamp:
							self.request_build ('Updated: %s' % path)

		local_sources = []
		artifact_stamp = None

		if not os.path.isfile (self.build_artifact):
			self.request_build("artifact doesn't exist")
		else:
			artifact_stamp = os.path.getmtime(self.build_artifact)

		is_updated (self._path)

		try:
			for source in self.sources:
				self.cd (build_root)
				resolved_source = None
				cache = None
				#if source.startswith ('http://'):
				#	raise Exception ('HTTP downloads are no longer allowed: %s', source)

				if source.startswith (('http://', 'https://', 'ftp://')):
					cache = get_download_dest (source)
					clean_func = checkout_archive (source, cache, workspace)
					resolved_source = workspace

				elif source.startswith (('git://','file://', 'ssh://')) or source.endswith ('.git'):
					cache = get_git_cache_path ()
					clean_func = checkout (self, source, cache, workspace)
					resolved_source =  workspace

				elif os.path.isabs (source) and os.path.isdir (source):
					trace ('copying local dir source %s ' % source)
					def clean_local_copy ():
						self.rm_if_exists (workspace)
					self.rm_if_exists (workspace)
					shutil.copytree (source, workspace)
					resolved_source = workspace
					self.resolve_version ()
					self.desc = '%s %s (local workspace: %s)' % (self.name, self.version, source)
					self.buildstring = ['local workspace: %s' % (source)]
					clean_func = clean_local_copy
				elif os.path.isfile (os.path.join (resource_dir, source)):
					resolved_source = os.path.join (resource_dir, source)
					self.buildstring.extend (['%s md5: %s' % (source, md5 (resolved_source))])

				if resolved_source is None:
					error ('could not resolve source: %s' % source)
				trace ('%s resolved to %s' % (source, resolved_source))

				local_sources.append (resolved_source)

			verbose ('\n\t'+ '\n\t'.join ([str for str in self.buildstring]))

			self.local_sources = local_sources
			if len(self.sources) != len(self.local_sources):
				error ('Source number mismatch after processing: %s before, %s after ' % (self.sources, self.local_sources))

			if clean_func is None:
				error ('workspace cleaning function (clean_func) must be set')

			return clean_func
		except Exception as e:
			if cache != None and os.path.exists (cache):
				self.rm (cache)
			if workspace != None and os.path.exists (workspace):
				self.rm (workspace)
			raise
		finally:
			self.cd (build_root)

	def request_build (self, reason):
		verbose (reason)
		self.needs_build = True

	def override_build (self, reason):
		verbose (reason)
		self.needs_build = False

	def start_build (self, arch):
			info (self.desc)
			protect_dir (self.staged_profile, recursive = True)

			workspace = self.workspace
			build_artifact = self.build_artifact

			if config.never_rebuild and os.path.isfile (build_artifact):
				if self.deploy_package (build_artifact, self.staged_profile):
					self.override_build ('never_rebuild option enabled, using artifact')
				else:
					warn ('Failed to deploy from artifact %s. Rebuilding' % os.path.basename (build_artifact))

			if self.needs_build:

				if (arch == 'darwin-universal' and self.needs_lipo):
					workspace_x86 = workspace +'-x86'
					workspace_x64 =workspace + '-x64'

					self.rm_if_exists (workspace_x86)
					self.rm_if_exists (workspace_x64)

					self.link (workspace, workspace_x86)
					shutil.copytree (workspace_x86, workspace_x64)

					package_stage = self.do_build ('darwin-32', workspace_x86)

					stagedir_x64 = self.do_build ('darwin-64', workspace_x64)

					print 'lipo', self.name

					self.lipo_dirs (stagedir_x64, package_stage, 'lib')
					self.copy_side_by_side (stagedir_x64, package_stage, 'bin', '64', '32')

				elif self.m32_only:
					package_stage = self.do_build ('darwin-32', workspace)
				else:
					package_stage = self.do_build (arch, workspace)

				self.make_artifact (package_stage, build_artifact)
			self.deploy_package (build_artifact, self.staged_profile)

	def deploy_package (self, artifact, dest):
		progress ('Deploying (%s -> %s)' % (os.path.basename(artifact), os.path.basename(dest)))

		unprotect_dir (dest, recursive = True)
		self.pushd (self.profile.build_root)
		artifact_stage = artifact + '.extracted'

		try:
			assert_exists (artifact)
			self.rm_if_exists (artifact_stage)
			unzip (artifact, artifact_stage)
			assert_exists (artifact_stage)
		except Exception as e:
			self.rm_if_exists (artifact)
			self.rm_if_exists (artifact_stage)
			protect_dir (dest, recursive = True)
			self.popd ()
			return False

		ensure_dir (artifact_stage)

		#catalogue files
		files = list()

		for path in iterate_dir (artifact_stage, summary = False):
			relpath = os.path.relpath (path, artifact_stage)
			destpath = os.path.join (dest, relpath)
			if os.path.exists (destpath) and not identical_files (path, destpath):
				warn ('deploy: Different file exists in package already: ''%s''' % relpath )
			files.append (relpath + '\n')

		files.sort ()
		if update (files, artifact + '.files'):
			warn ('Package filelist changed')

		if len (files) != 0:
			merge_trees (artifact_stage, dest, False)

		self.deploy ()
		self.popd ()

		self.rm_if_exists (artifact_stage)

		protect_dir (dest, recursive = True)

		os.utime (artifact, None)
		return True

	def do_build (self, arch, workspace_dir):
		progress ('Building (arch: %s)' % (arch))

		self.stage_root  = os.path.join (workspace_dir + '.stage')
		self.rm_if_exists (self.stage_root)
		self.staged_prefix = os.path.join (self.stage_root, self.package_prefix [1:])

		os.makedirs (self.staged_prefix)

		# protect against relocation bugs often landing files in the wrong path
		protect_dir (self.stage_root)
		self.pushd (workspace_dir)
		if self.profile.verbose:
			self.verbose = True #log sh() uses while in package logic
		try:
			self.prep ()
			self.arch_build (arch)
			self.build_env = self.expand_build_env ()
			self.build ()
			self.install ()

			if not os.path.exists (self.staged_prefix):
				error ('Result directory %s not found.' % self.staged_prefix)

			self.profile.process_package (self)

			if not self.dont_clean:
				retry (self.clean)
			self.popd()
		except Exception as e:
			self.popd (failure = True)
			self.rm_if_exists (self.stage_root)

			if os.path.exists (workspace_dir):
				problem_dir = os.path.join (self.profile.root, os.path.basename (workspace_dir) + '.problem')

				#take this chance to clear out older .problems
				for d in os.listdir (self.profile.root):
					if d.endswith ('.problem'):
						self.rm (os.path.join(self.profile.root, d))

				shutil.move (workspace_dir, problem_dir)
				info ('Build moved to ./%s \n Run "source ./%s" first to replicate bockbuild environment.' % (os.path.basename (problem_dir), os.path.basename (self.profile.envfile)))
			if e is CommandException:
				error (str(e))
			raise
		finally:
			if os.path.exists (self.stage_root):
				unprotect_dir (self.stage_root)

		self.verbose = False

		return self.staged_prefix


	def make_artifact (self, stage_dir, build_artifact):
		self.rm_if_exists (build_artifact)
		zip (stage_dir, build_artifact)
		self.rm_if_exists (stage_dir)

	def deploy (self):
		return

	def process (self, func, directory, error_func, error_message ):
		popped = False
		try:
			self.pushd (directory)
			func ()
		except Exception as e:
			self.popd (failure = True)
			popped = True

			if e is BockbuildException:
				error ('%s: %s' % (func.__name__ , e.message))
			warn (str(e))
			warn (error_message)
			error_func ()
		finally:
			if not popped:
				self.popd()


	def sh (self, *commands):
		for command in commands:
			try:
				env_command = '%s %s' % (self.build_env, expand_macros (command, self))
			except Exception as e:
				error ('MACRO EXPANSION ERROR: ' + str(e))
			if self.verbose is True:
				logprint ('\t@\t' + expand_macros (command, self), bcolors.BOLD)

			stdout = tempfile.NamedTemporaryFile()
			stderr = tempfile.NamedTemporaryFile()
			full_command = '%s  > %s 2> %s' % (env_command, stdout.name, stderr.name)
			try:
				run_shell (full_command)
			except Exception as e:
				output_text = stdout.readlines ()
				if len(output_text) > 0:
					warn ('stdout:')
					for line in output_text:
						print line,
				error_text = stderr.readlines ()
				if len(error_text) > 0:
					warn ('stderr:')
					for line in error_text:
						print line,
				warn('path: ' + os.getcwd ())
				warn('build env: ' + self.build_env)
				raise CommandException ('command failed: %s' % expand_macros (command, self))
			finally:
				stdout.close ()
				stderr.close ()

	def backtick (self, command):
		command = expand_macros (command, self)
		return backtick (command)

	def cwd (self):
		try:
			self._cwd = os.getcwd ()
		except Exception as e:
			warn ('In invalid directory')
			if not self._cwd:
				error ('No last known directory, cannot recover')

			warn ('Switching to last known directory: %s ' % self._cwd)
			os.chdir (self._cwd)

		return self._cwd

	def cd (self, dir):
		dir = expand_macros (dir, self)

		if self.cwd () == dir:
			return

		os.chdir (dir)
		self.cwd ()
		trace (dir)


	def pushd (self, dir):
		if len(self._dirstack) == 0:
			self._dirstack.append ( {'dir' : self._cwd, 'caller' : 'profile'})

		self.cd (dir)
		self._dirstack.append ( {'dir' : self._cwd, 'caller' : get_caller () })

	def popd (self, failure = False):
		caller = get_caller ()

		cwd = self._dirstack.pop ()

		if cwd['caller'] != caller:
				warn ('popd: Unmatched pushd/popd callers: (%s/%s)' % (cwd['caller'], caller))
				#return False

		if cwd['dir'] !=  self.cwd () and not failure:
				warn ('popd: Inconsistent current dir state (expected ''%s'', was in ''%s''' % (cwd['dir'], self._cwd))

		top = self._dirstack[-1]

		self.cd (top['dir'])

	def prep (self):
		return

	def rm_if_exists (self, path):
		path = expand_macros (path, self)
		if os.path.exists (path):
			self.rm (path)

	def rm (self, path):
		trace (path)
		delete (expand_macros (path, self))

	def link (self, source, link):
		trace('%s -> %s' % (link, source))
		source = expand_macros (source, self)
		link = expand_macros (link, self)
		if os.path.exists (link):
			 self.rm(link)
		os.symlink (source, link)

	def extract_archive (self, archive, validate_only, overwrite=False):
		self.pushd (self.profile.build_root)
		try:
			self.tar = os.path.join (Package.profile.toolchain_root, 'bin', 'tar')
			if not os.path.exists (self.tar):
				self.tar = 'tar'
			root, ext = os.path.splitext (archive)
			command = None
			if ext == '.zip':
				flags = ["-qq"]
				if overwrite:
					flags.extend(["-o"])
				if validate_only:
					flags.extend(["-t"])
				command = ' '.join(['unzip'] + flags + [archive])
				if validate_only:
					command = command + ' > /dev/null'
			else:
				command = '%{tar} xf ' + archive
				if validate_only:
					command = command + ' -O > /dev/null'
			self.sh (command)
		finally:
			self.popd ()

	def build (self):
		Package.configure (self)
		Package.make (self)

	def lipo_dirs (self, dir_64, dir_32, bin_subdir, replace_32 = True): 
		dir64_bin = os.path.join (dir_64, bin_subdir)
		dir32_bin = os.path.join (dir_32, bin_subdir)
		lipo_dir = tempfile.mkdtemp()
		lipo_bin = os.path.join (lipo_dir, bin_subdir)

		if not os.path.exists (dir64_bin):
			return # we don't always have bin/lib dirs

		if not os.path.exists (lipo_bin):
				os.mkdir (lipo_bin)

		#take each 64-bit binary, lipo with binary of same name

		for root,dirs,filelist in os.walk(dir64_bin):
			relpath = os.path.relpath (root, dir64_bin)
			for file in filelist:
				if file.endswith ('.a') or file.endswith ('.dylib') or file.endswith ('.so'):
					dir64_file = os.path.join (dir64_bin, relpath, file)
					dir32_file = os.path.join (dir32_bin, relpath, file)
					lipo_file = os.path.join (lipo_bin, relpath, file)
					if os.path.exists (dir32_file):
						if not os.path.exists (os.path.join (lipo_bin, relpath)):
							os.makedirs (os.path.join (lipo_bin, relpath))

						if os.path.islink (dir64_file):
							continue
						lipo_cmd = 'lipo -create %s %s -output %s ' % (dir64_file, dir32_file, lipo_file) 
						#print lipo_cmd
						run_shell(lipo_cmd)
						if replace_32:
							#replace all 32-bit binaries with the new fat binaries
							shutil.copy2 (lipo_file, dir32_file)
					else:
						warn ("lipo: 32-bit version of file %s not found"  %file)

	def copy_side_by_side (self, src_dir, dest_dir, bin_subdir, suffix, orig_suffix =  None):
		def add_suffix (filename, sfx):
			fileparts = filename.split ('.', 1)
			if len (fileparts) > 1:
				p = '%s%s.%s' % (fileparts[0], sfx, fileparts[1])
			else:
				p = '%s%s' % (filename, sfx)

			trace(p)
			return p

		src_dir = os.path.join (src_dir, bin_subdir)
		dest_dir = os.path.join (dest_dir, bin_subdir)
		trace ('src_dir %s' % src_dir)
		trace ('dest_dir %s' % dest_dir)

		if not os.path.exists (src_dir):
			return # we don't always have bin/lib dirs

		for path in iterate_dir(src_dir):
			relpath = os.path.relpath (path, src_dir)
			reldir, filename = os.path.split (relpath)
			trace (reldir + '/' + filename)

			filetype = backtick ('file -b "%s"' % path)[0]
			if filetype.startswith('Mach-O'):
				dest_file = os.path.join (dest_dir, reldir, add_suffix(filename, suffix))
				trace (dest_file)
				dest_orig_file = os.path.join (dest_dir, reldir, filename)

				if not os.path.exists (dest_orig_file):
					error ('lipo: %s exists in %s but not in %s' % (relpath, src_dir, dest_dir))
				if orig_suffix != None:
					suffixed = os.path.join (dest_dir, reldir, add_suffix (filename, orig_suffix))
					trace (suffixed)
					shutil.move (dest_orig_file, suffixed)
					os.symlink (os.path.basename (suffixed), dest_orig_file)

				shutil.copy2 (path, dest_file)

	def arch_build (self, arch):
		Package.profile.arch_build (arch, self)

	def expand_build_env (self):
		return expand_macros (
		'OBJCFLAGS="%{gcc_flags} %{local_gcc_flags}" '
		'CFLAGS="%{gcc_flags} %{local_gcc_flags}" '
		'CXXFLAGS="%{gcc_flags} %{local_gcc_flags}" '
		'CPPFLAGS="%{cpp_flags} %{local_cpp_flags}" '
		'LDFLAGS="%{ld_flags} %{local_ld_flags}" ', self)

	def configure (self):
		self.sh ('%{configure} %{configure_flags} %{local_configure_flags}')

	def make (self):
		self.sh ('%{make}')

	def install (self):
		self.sh ('%{makeinstall}')

Package.default_sources = None

# -------------------------------------
# Package Templates
# -------------------------------------

class GnomePackage (Package):
	def __init__ (self, name, version_major = '0', version_minor = '0',
		configure_flags = None, sources = None, override_properties = None):

		self.version_major = version_major
		self.version_minor = version_minor

		Package.__init__ (self, name, '%{version_major}.%{version_minor}',
			configure_flags = configure_flags,
			sources = sources,
			override_properties = override_properties)

GnomePackage.default_sources = [
	'http://ftp.gnome.org/pub/gnome/sources/%{name}/%{version_major}/%{name}-%{version}.tar.bz2'
]

class GnomeXzPackage (GnomePackage): pass

GnomeXzPackage.default_sources = [
	'http://ftp.gnome.org/pub/gnome/sources/%{name}/%{version_major}/%{name}-%{version}.tar.xz'
]

class GnomeGitPackage (Package):
	def __init__ (self, name, version, revision,
		configure_flags = None, sources = None, override_properties = None):
		Package.__init__ (self, name, version,
			configure = './autogen.sh --prefix="%{package_prefix}"',
			configure_flags = configure_flags,
			sources = sources,
			override_properties = override_properties,
			revision = revision)

GnomeGitPackage.default_sources = [
	'git://git.gnome.org/%{name}'
]

class GnuPackage (Package): pass
GnuPackage.default_sources = [
    'ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz'
]

class GnuBz2Package (Package): pass
GnuBz2Package.default_sources = [
    'ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2'
]

class GnuXzPackage (Package): pass
GnuXzPackage.default_sources = [
    'ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz'
]

class CairoGraphicsPackage (Package): pass
CairoGraphicsPackage.default_sources = [
	'http://cairographics.org/releases/%{name}-%{version}.tar.gz'
]

class CairoGraphicsXzPackage (Package): pass
CairoGraphicsXzPackage.default_sources = [
	'http://cairographics.org/releases/%{name}-%{version}.tar.xz'
]

class ProjectPackage (Package):
	def __init__ (self, project, name, version, configure_flags = None,
		sources = None, override_properties = None):

		self.project = project
		Package.__init__ (self, name, version,
			configure_flags = configure_flags,
			sources = sources,
			override_properties = override_properties)

class SourceForgePackage (ProjectPackage): pass
SourceForgePackage.default_sources = [
	'https://downloads.sourceforge.net/sourceforge/%{project}/%{name}-%{version}.tar.gz'
]

class FreeDesktopPackage (ProjectPackage): pass
FreeDesktopPackage.default_sources = [
	'http://%{project}.freedesktop.org/releases/%{name}-%{version}.tar.gz'
]

class GitHubTarballPackage (Package):
	def __init__ (self, org, name, version, commit, configure, override_properties = None):
		Package.__init__ (self, name, version, revision = commit, organization = org,
			override_properties = override_properties)
		self.configure = configure
		self.source_dir_name = '%s-%s-%s' % ( org, name, self.revision[:7] )
GitHubTarballPackage.default_sources = [
	'https://github.com/%{organization}/%{name}/tarball/%{revision}'
]

class GitHubPackage (Package):
	def __init__ (self, organization, name, version, revision = None, git_branch = None, configure = None, configure_flags = None, override_properties = None):
		Package.__init__ (self, name, version,
			organization = organization,
			revision = revision,
			git_branch = git_branch,
			configure_flags = configure_flags,
			configure = configure,
			sources = ['git://github.com/%{organization}/%{name}.git'],
			override_properties = override_properties)


class GstreamerPackage (ProjectPackage): pass
GstreamerPackage.default_sources = [
	'https://%{project}.freedesktop.org/src/%{name}/%{name}-%{version}.tar.gz'
]

class XiphPackage (ProjectPackage): pass
XiphPackage.default_sources = [
	'https://downloads.xiph.org/releases/%{project}/%{name}-%{version}.tar.gz'
]
