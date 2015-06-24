import hashlib
import os
import sys
import shutil
import tempfile
import filecmp
import datetime
import stat
from urllib import FancyURLopener
from util.util import *

class Package:
	def __init__ (self, name, version, organization = None, configure_flags = None, sources = None, revision = None, git_branch = 'master', source_dir_name = None, override_properties = None, configure = None):
		Package.last_instance = self

		self._dirstack = []
		self.verbose = False

		self.name = name
		self.version = version
		self.organization = organization

		self.configure_flags = ['--enable-debug']

		self.gcc_flags = list(Package.profile.gcc_flags)
		self.cpp_flags = list(Package.profile.gcc_flags)
		self.ld_flags = list(Package.profile.ld_flags)

		self.local_cpp_flags = []
		self.local_gcc_flags = []
		self.local_ld_flags = []
		self.local_configure_flags = []

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
		self.stage_root = Package.profile.stage_root
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

		if self.build_dependency:
			self.package_prefix = Package.profile.toolchain_root
			self.staged_prefix = Package.profile.toolchain_root
			self.makeinstall = self.makeinstall or 'make install'
			#self.ld_flags = '-L%{staged_prefix}/lib' # XXX
		else:
			self.package_prefix = Package.profile.prefix
			self.staged_prefix = Package.profile.staged_prefix
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

	def get_package_string (self):
		str = self.name
		if self.version:
			str+= ' v.' + self.version
		if self.revision:
			str+= ' (rev. ' + self.revision + ')'
		return str

	def _fetch_sources (self, build_root, workspace, resource_dir, source_cache_dir):
		clean_func = None # what to run if the workspace needs to be redone

		def clean_nop ():
			pass

		def checkout (self, source_url, cache_dir, workspace_dir):
			def clean_git_workspace ():
				print 'Cleaning git workspace:', self.name
				self.pushd (workspace_dir)
				self.sh ('%{git} reset --hard')
				self.sh ('%{git} clean -xffd')
				self.popd ()

			# Explicitly reset the working dir to a known directory which has not been deleted
			# 'git clone' does not work if you are in a directory which has been deleted
			os.chdir (build_root)
			if not os.path.exists (cache_dir):
				# since this is a fresh cache, the workspace copy is invalid if it exists
				if os.path.exists (workspace_dir):
					self.rm (workspace_dir)
				print 'Cloning git repo: %s' % source_url
				self.sh ('%' + '{git} clone --mirror "%s" "%s"' % (source_url, cache_dir))
				
			log (1, 'Updating cache')
			self.pushd (cache_dir)
			if self.git_branch == None:
				self.sh ('%{git} fetch --all --prune')
			else:
				self.sh ('%' + '{git} fetch origin %s' % self.git_branch)
			self.popd ()

			if not os.path.exists(workspace_dir):
				log (1, 'Cloning a fresh workspace')
				self.sh ('%' + '{git} clone --local --shared 	"%s" "%s"' % (cache_dir, workspace_dir))
				self.cd (workspace_dir)
				clean_func = clean_nop
			else:
				clean_func = clean_git_workspace

			log (1, 'Updating workspace')
			self.cd (workspace_dir)

			if self.git_branch == None:
				self.sh ('%{git} fetch --all --prune')
			else:
				self.sh ('%' + '{git} fetch origin %s:refs/remotes/origin/%s' % (self.git_branch, self.git_branch))

			self.sh ('%{git} reset')

			current_revision = self.backtick ('%{git} rev-parse HEAD')[0]

			if self.revision != None:
				target_revision = self.revision
			else:
				if self.git_branch == None:
					warn ('Package does not define revision or branch, defaulting to tip of "master"')
				self.git_branch = self.git_branch or 'master'
				target_revision = self.backtick ('%' +'{git} rev-parse origin/%s' % self.git_branch)[0]

			if (current_revision != target_revision):
				self.sh ('%{git} reset --hard')
				self.sh ('%{git} clean -xffd')
				self.sh ('%' + '{git} checkout %s' % target_revision)

			current_revision = self.backtick ('%{git} rev-parse HEAD')[0]

			if (self.revision != None and self.revision != current_revision):
				raise Exception ('Workspace error: Revision is %s, package specifies %s' % (current_revision, self.revision))

			self.revision = current_revision
			return clean_func


		def get_download_dest(url):
			return os.path.join (source_cache_dir, os.path.basename (url))

		def get_git_cache_path ():
			if self.organization is None:
				name = self.name
			else:
				name = self.organization + "+" + self.name
			return os.path.join (source_cache_dir, name)

		local_sources = []
		cache = None

		self.cd (build_root)

		try:
			for source in self.sources:
				#if source.startswith ('http://'):
				#	raise Exception ('HTTP downloads are no longer allowed: %s', source)

				if source.startswith (('http://', 'https://', 'ftp://')):
					archive = source
					cache = get_download_dest (archive)

					def checkout_archive (archive, cache, workspace):
						self.pushd (build_root)
						if not os.path.exists (cache):
							# since this is a fresh cache, the workspace copy is invalid if it exists
							if os.path.exists (workspace):
								self.rm (workspace)
							progress ('Downloading: %s' % archive)
							filename, message = FancyURLopener ().retrieve (archive, cache)
						if not os.path.exists (workspace):
							self.extract_archive (cache, False)
							os.utime (workspace, None)
							clean_func = clean_nop
						else:
							clean_func = clean_archive
						if not os.path.exists (workspace):
							raise Exception ('Archive %s was extracted but not found at workspace path %s' % (cache, workspace))							
						self.popd ()
						return clean_func

					def clean_archive ():
						print 'Re-extracting archive: ' + self.name + ' ('+ archive + ')'
						try:
							self.rm (workspace)
							checkout_archive (archive, cache, workspace)
						except Exception as e:
							if os.path.exists (cache):
								self.rm (cache)
							if os.path.exists (workspace):
								self.rm (workspace)
							raise e

					clean_func = checkout_archive (archive, cache, workspace)
					local_sources.append (workspace)

				elif source.startswith (('git://','file://', 'ssh://')) or source.endswith ('.git'):
					cache = get_git_cache_path ()
					clean_func = checkout (self, source, cache, workspace)
					local_sources.append (workspace)
				elif os.path.isfile (os.path.join (resource_dir, source)):
					#local_source_file = os.path.basename (local_source)
					#cache = get_local_filename (local_source)
					#print 'local_source', local_source
					#print 'cache', cache

					#if not filecmp.cmp(local_source, cache):
					#	log (1, 'copying local source: %s -> %s' % (local_source_file, cache))
					#	shutil.copy2 (local_source, cache)
					#	local_sources.append (cache)
					#else:
					local_sources.append (os.path.join (resource_dir, source))
				else:
					raise Exception ('could not resolve source: %s' % source)

			self.local_sources = local_sources
			if len(self.sources) != len(self.local_sources):
				error ('Source number mismatch after processing: %s before, %s after ' % (self.sources, self.local_sources))

			if clean_func is None:
				error ('workspace cleaning function (clean_func) must be set')

			package_version = expand_macros (self.version, self)
			found_version = self.try_get_version (workspace) or package_version
			if found_version[0] != package_version[0]:
				warn ('Version in configure.ac is %s, package declares %s' % (found_version, package_version))
			self.version = package_version

			info (self.get_package_string ())

			return clean_func
		except Exception as e:
			if cache != None and os.path.exists (cache):
				self.rm (cache)
			if workspace != None and os.path.exists (workspace):
				self.rm (workspace)
			raise

	def is_successful_build(self, success_file):
		if not os.path.exists (success_file):
			return False
		mtime = os.path.getmtime(success_file)
		newer = True
		src = list(self.local_sources)
		src.append (self._path)
		for s in (src):
			src_txt = 'Source: %s' % s
			if os.path.getmtime(s) > mtime:
				src_txt = src_txt +  ' (Changed)'
				newer = False
			info (src_txt)
 			
 			# FIXME: There seem to be lots of dirs being touched from other processes.
 			# Must investigate, but turn off subdir checking for now

			# elif os.path.isdir (s): 
			# 	for root, dirs, files in os.walk (s):
			# 		dirs[:] = [d for d in dirs if not d[0] == '.'] # http://stackoverflow.com/questions/13454164/os-walk-without-hidden-folders
			# 		for dir in dirs:
			# 			dir_path = os.path.join (root, dir)
			# 			if os.path.isdir(dir_path) and os.path.getmtime(dir_path) > mtime:
			# 				print 'Updated source: %s' % dir_path
			# 				newer = False
		return newer

	def fetch (self):
		expand_macros (self.sources, self)
		self.source_dir_name = expand_macros (self.source_dir_name, self)
		profile = Package.profile
		self.workspace = os.path.join (profile.build_root, self.source_dir_name)

		return self._fetch_sources (profile.build_root, self.workspace, profile.resource_root, profile.source_cache)

	def start_build (self, install_root, stage_root, arch):			
			profile = Package.profile

			clean_func = retry (self.fetch)

			workspace = self.workspace

			lipo_build = (arch == 'darwin-universal' and self.needs_lipo)

			build_artifact = os.path.join (profile.build_root, self.name + '.artifact')
			if self.is_successful_build(build_artifact):
				progress ('Installing %s' % self.name)

				if lipo_build:
					stagedir = os.path.join (workspace, 'lipo-stage', install_root [1:])
					run_shell('rsync -a --ignore-existing %s/* %s' % (stagedir, profile.staged_prefix), False)

				else:
					os.chdir (workspace)
					self.install ()
			else:
				try:
					retry (clean_func)

					if lipo_build == True:

						workspace_x86 = os.path.join (workspace, 'x86')
						workspace_x64 = os.path.join (workspace, 'x64')

						shutil.move (workspace, workspace + 'tmp')
						os.makedirs (workspace)
						shutil.move (workspace + 'tmp', workspace_x86) # package/x86	
						shutil.copytree (workspace_x86, workspace_x64) # package/x64

						stagedir_lipo = self.do_build ('darwin-32', install_root, workspace_x86, os.path.join (workspace, 'lipo-stage')) #package/lipo-stage

						stagedir_x64 = self.do_build ('darwin-64', install_root, workspace_x64)

						print 'lipo', self.name

						self.lipo_dirs (stagedir_x64, stagedir_lipo, 'lib')							
						self.copy_side_by_side (stagedir_x64, stagedir_lipo, 'bin', '64', '32')
						run_shell('rsync -a --ignore-existing %s/* %s' % (stagedir_lipo, profile.staged_prefix), False)

						# staging steps needs to be fixed for package staged_prefix'es being different than profile's
						self.staged_prefix = profile.staged_prefix

					elif self.m32_only:
						self.do_build ('darwin-32', install_root, workspace, stage_root)
					else:
						self.do_build (arch, install_root, workspace, stage_root)
				except Exception as e:
					if os.path.exists (workspace):
						problem_dir = os.path.basename (workspace) + '.problem'
						shutil.rmtree (os.path.join (self.profile.root,  problem_dir), ignore_errors = True)
						shutil.move (workspace,
							os.path.join (self.profile.root,  problem_dir))
						warn (str (e))
						error ('Failed build at ./%s \n Run "source ./%s" first to replicate bockbuild environment.' % (problem_dir, os.path.basename (self.profile.envfile)))

				self.make_artifact (profile.staged_prefix, build_artifact)
				
			if not self.build_dependency:
				self.stage (profile.staged_prefix)

			# self.deploy ()


	def do_build (self, arch, install_prefix, workspace_dir, stage_root = None):

		progress ('Building (arch: %s)' % (arch))

		if stage_root == None:
			stage_root = workspace_dir + '-stage'

		self.cd (workspace_dir)
		self.stage_root  = stage_root
		if install_prefix == stage_root:
			self.staged_prefix = install_prefix
		else:
			self.staged_prefix = os.path.join (stage_root, install_prefix [1:])
		self.package_prefix = install_prefix

		if self.profile.verbose:
			self.verbose = True #log sh() uses while in package logic
		self.arch_build (arch)
		self.prep ()
		self.build ()
		self.install ()

		self.verbose = False 
		return self.staged_prefix
			

	def make_artifact (self, stage_dir, build_artifact):
		open (build_artifact, 'w').close ()
		os.utime (build_artifact, None)
		
		return

	def sh (self, *commands):
		for command in commands:
			try:
				env_command = expand_macros (self.env() + command, self)
			except Exception as e:
				error ('MACRO EXPANSION ERROR: ' + str(e))
			if self.verbose is True:
				print bcolors.BOLD + '\n\t@\t' + expand_macros (command, self) + bcolors.ENDC

			stdout = tempfile.NamedTemporaryFile()
			stderr = tempfile.NamedTemporaryFile()
			full_command = '%s  > %s 2> %s' % (env_command, stdout.name, stderr.name)
			try:
				run_shell (full_command)
			except Exception as e:
				output_text = stdout.readlines ()
				if len(output_text) > 0:
					warn ('stdout (last 50 lines):')
					for line in output_text[-50:]:
						print line,
				error_text = stderr.readlines ()
				if len(error_text) > 0:
					warn ('stderr:')
					for line in error_text:
						print line,
				warn('path: ' + os.getcwd ())
				warn('full command: ' + env_command)
				raise Exception ('command failed: %s' % command)
			finally:
				stdout.close ()
				stderr.close ()

	def backtick (self, command):
		command = expand_macros (command, self)
		return backtick (command)

	def cd (self, dir):
		dir = expand_macros (dir, self)
		log (1, 'cd "%s"' % dir)
		os.chdir (dir)

	def pushd (self, dir):
		self._dirstack.append (os.getcwd ())
		self.cd (dir)

	def popd (self):
		self.cd (self._dirstack.pop ())

	def prep (self):
		return

	def rm (self, path):
		log (1, 'deleting %s' % path)
		path = expand_macros (path, self)
		if os.path.isfile (path) or os.path.islink (path):
			os.remove (path)
		elif os.path.isdir (path):
			shutil.rmtree (path, ignore_errors=False)
		else:
			raise Exception ('Invalid path to rm: %s' % path)


	def link (self, source, link):
		log (1, 'linking %s -> %s' % (link, source))
		source = expand_macros (source, self)
		link = expand_macros (link, self)
		if os.path.exists (link):
			 self.rm(link)
		os.symlink (source, link)

	def extract_archive (self, archive, validate_only, overwrite=False):
		self.pushd (self.profile.build_root)
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
		src_dir = os.path.join (src_dir, bin_subdir)
		dest_dir = os.path.join (dest_dir, bin_subdir)

		if not os.path.exists (src_dir):
			return # we don't always have bin/lib dirs

		for root,dirs,filelist in os.walk(src_dir):
			relpath = os.path.relpath (root, src_dir)
			for file in filelist:
				src_file = os.path.join (src_dir, relpath, file)
				if os.path.islink (src_dir):
					continue

				filetype = backtick ('file -b "%s"' % src_file)[0]
				if filetype.startswith('Mach-O'):
					dest_file = os.path.join (dest_dir, relpath, file + suffix) #FIXME: perhaps add suffix before any .'s
					dest_orig_file = os.path.join (dest_dir, relpath, file)
					if orig_suffix != None and os.path.exists (dest_orig_file):
						shutil.move (dest_orig_file, dest_orig_file + orig_suffix)
						os.symlink (os.path.basename (dest_orig_file + orig_suffix), dest_orig_file)

					shutil.copy2 (src_file, dest_file)

	def stage_pkgs (self, pkg_dir):
		log (1, 'Staging pkg-config packages')
		for root,dirs,filelist in os.walk (pkg_dir):
			for file in filelist:
				if file.endswith ('.pc'):
					self.stage_file (os.path.join (root, file))

	def stage_file (self, path):
		path = expand_macros (path, self)
		if os.path.exists (path + '.release'):
			return
		with open(path) as text:
			output = open(path + '.stage', 'w')
			for line in text:
				tokens = line.split (" ")
				for idx,token in enumerate(tokens):
					if  token.find (self.staged_prefix) == -1:
						tokens[idx] = token.replace(self.profile.prefix,self.profile.staged_prefix)
					else:
						tokens[idx] = token.replace(self.staged_prefix,self.profile.staged_prefix)

				output.write (" ".join(tokens))
			output.close
		shutil.move (path, path + '.release')
		shutil.move (path + '.stage', path)
		os.chmod (path, os.stat (path + '.release').st_mode)
		self.profile.staged_textfiles.append (path)


	def stage_binaries (self, dir):
		def abort_staging (path):
			os.remove (path)
			shutil.copy (path + '.release', path)
		for root,dirs,filelist in os.walk (dir):
			for file in filelist:
				path = os.path.join (root, file)
				if path.endswith ('.release') or os.path.exists (path + '.release'):
					continue
				if os.path.islink (path):
					continue

				filetype = backtick ('file -b "%s"' % path)[0]
				if filetype.startswith('Mach-O') and not path.endswith ('.a'):
					shutil.copy (path, path + '.release')
					try:
						staged_path = os.path.join (self.profile.staged_prefix, dir, os.path.relpath (path, dir))
						run_shell ('install_name_tool -id %s %s' % (staged_path, path))
					except:
						warn ('Staging failed for %s' % os.path.relpath (path,dir))
						abort_staging (path)
						continue
					libs = backtick ('otool -L %s' % path)
					for line in libs:
						#parse 'otool -L'
						if not line.startswith ('\t'):
							continue
						rpath = line.strip ().split(' ')[0]
						if rpath.find (self.profile.prefix) != -1:
							if rpath.find (self.staged_prefix) == -1:
								remap = rpath.replace (self.profile.prefix, self.profile.staged_prefix)
							else:
								remap = rpath.replace (self.staged_prefix, self.profile.staged_prefix)
							try:
								run_shell ('install_name_tool -change %s %s %s' % (rpath, remap, path))
							except:
								warn ('Staging failed for %s' % os.path.relpath (path,dir))
								abort_staging (path)
								continue
					self.profile.staged_binaries.append (path)
				elif filetype.endswith ('text executable'):
					self.stage_file (path)

	def stage_la_files (self, lib_dir):
		log (1, 'Staging .la files')
		for root,dirs,filelist in os.walk (lib_dir):
			for file in filelist:
				if file.endswith ('.la'):
					self.stage_file (os.path.join (root, file))


	def arch_build (self, arch):
		Package.profile.arch_build (arch, self)

	def env (self):
		return str('OBJCFLAGS="%{gcc_flags} %{local_gcc_flags}" '
		'CFLAGS="%{gcc_flags} %{local_gcc_flags}" '
		'CXXFLAGS="%{gcc_flags} %{local_gcc_flags}" '
		'CPPFLAGS="%{cpp_flags} %{local_cpp_flags}" '
		'LDFLAGS="%{ld_flags} %{local_ld_flags}" ')

	def configure (self):
		self.sh ('%{configure} %{configure_flags} %{local_configure_flags}')

	def make (self):
		self.sh ('%{make}')

	def install (self):
		self.sh ('%{makeinstall}')

	def stage (self, dir, stage_to_dir = dir):
		self.stage_la_files (os.path.join(dir, 'lib'))
		self.stage_pkgs (os.path.join (dir, 'share', 'pkgconfig'))
		self.stage_pkgs (os.path.join (dir, 'lib', 'pkgconfig'))
		self.stage_binaries  (os.path.join(dir, 'lib'))
		self.stage_binaries (os.path.join(dir, 'bin'))

		for extra_file in self.extra_stage_files:
			self.stage_file (os.path.join (dir, extra_file))


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
