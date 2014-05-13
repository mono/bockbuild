import hashlib
import os
import sys
import shutil
import tempfile
import filecmp
import datetime
from urllib import FancyURLopener
from util.util import *

class Package:
	def __init__ (self, name, version, organization = None, configure_flags = None, sources = None, revision = None, git_branch = 'master', source_dir_name = None, override_properties = None, configure = None):
		Package.last_instance = self

		self._dirstack = []

		self.name = name
		self.version = version
		self.organization = organization

		self.configure_flags = ['--enable-debug']

		self.gcc_flags = Package.profile.gcc_flags
		self.cpp_flags = Package.profile.gcc_flags
		self.ld_flags = Package.profile.ld_flags

		self.local_cpp_flags = []
		self.local_gcc_flags = []
		self.local_ld_flags = []
		self.local_configure_flags = []

		# fat binary parameters. On a 64-bit Darwin profile (m64 = True) 
		# each package must decide if it will a) perform a multi-arch (64/32) build 
		# b) request two builds that are lipoed at the end or c) request a 32-bit
		# build only.

		self.m64 = Package.profile.m64
		self.fat_build = False
		self.needs_lipo = False
		self.m32_only = False
		self.build_dependency = False

		if Package.profile.global_configure_flags:
			self.configure_flags.extend (Package.profile.global_configure_flags)
		if configure_flags:
			self.configure_flags.extend (configure_flags)

		self.sources = sources
		if self.sources == None \
			and not self.__class__.default_sources == None:
			self.sources = list (self.__class__.default_sources)

		if self.organization == None:
			self.organization = self.extract_organization (self.sources[0])

		self.source_dir_name = source_dir_name
		if self.source_dir_name == None:
			self.source_dir_name = '%{name}-%{version}'

		self.revision = revision

		self.prefix = Package.profile.prefix

		if configure:
			self.configure = configure
		else:
			self.configure = './configure --prefix="%{package_prefix}"'

		self.make = 'make -j%s' % Package.profile.cpu_count
		self.makeinstall = 'make install'
		self.git = 'git'
		self.git_branch = git_branch
		for git in ['/usr/local/bin/git', '/usr/local/git/bin/git', '/usr/bin/git']:
			if os.path.isfile (git):
				self.git = git
				break

		if not override_properties == None:
			for k, v in override_properties.iteritems ():
				self.__dict__[k] = v

		self._sources_dir = None
		self._package_dir = None

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

	def _fetch_sources (self, workspace, package_dir, package_dest_dir):

		def checkout (self, source_url, cache_dir, workspace_dir):
			if not os.path.exists (cache_dir):
				print 'No cache detected. Cloning a fresh cache'
				self.sh ('%' + '{git} clone --mirror "%s" "%s"' % (source_url, cache_dir))
			else:
				print 'Updating existing cache'
				self.cd (cache_dir)
				self.sh ('%{git} fetch --all --prune')

			if not os.path.exists(workspace_dir):
				print 'No workspace checkout detected. Cloning a fresh workspace checkout from the cache'
				self.sh ('%' + '{git} clone --local --shared "%s" "%s"' % (cache_dir, workspace_dir))
				self.cd (workspace_dir)
			else:
				print 'Updating existing workspace checkout'
				self.cd (workspace_dir)
				self.sh ('%{git} clean -xffd')
				self.sh ('%{git} reset --hard')
				self.sh ('%{git} fetch --all --prune')

			if self.revision != None:
				self.sh ('%' + '{git} checkout %s' % self.revision)
			elif self.git_branch != None:
				self.sh ('%' + '{git} checkout origin/%s' % self.git_branch)
			else:
				self.sh ('%{git} checkout origin/master')

		def get_local_filename(source):
			return source if os.path.isfile(source) else os.path.join (package_dest_dir, os.path.basename (source))

		def get_cache_name (name):
			if self.organization is None:
				return self.name
			else:
				return self.organization + "+" + name

		if self.sources is None:
			return

		if not os.path.exists (package_dest_dir):
			os.mkdir (package_dest_dir)

		local_sources = []
		for source in self.sources:
			local_source = os.path.join (package_dir, source)
			local_source_file = os.path.basename (local_source)
			local_dest_file = get_local_filename (local_source)
			local_sources.append (local_dest_file)

			if os.path.isfile (local_source):
				if filecmp.cmp(local_source, local_dest_file):
					log (1, 'using cached source: %s' % local_dest_file)
				else:
					log (1, 'copying local source: %s' % local_source_file)
					shutil.copy2 (local_source, local_dest_file)
			elif source.startswith (('http://', 'https://', 'ftp://')):
				if os.path.isfile(local_dest_file):
					try:
						self.extract_archive (local_dest_file, True)
						log (1, 'using cached source: %s' % local_dest_file)
					except:
						log (1, 'local cache is corrupt for: %s' % local_dest_file)
						os.remove (local_dest_file)

				if not os.path.isfile(local_dest_file):
					log (1, 'downloading remote source: %s' % source)
					filename, message = FancyURLopener ().retrieve (source, local_dest_file)

			elif source.startswith (('git://','file://', 'ssh://')) or source.endswith ('.git'):
				log (1, 'cloning or updating git repository: %s' % source)
				local_name = os.path.splitext(os.path.basename(source))[0]
				local_dest_file = os.path.join (package_dest_dir, '%s.gitmirror' % (get_cache_name (local_name)))

				local_sources.pop ()
				local_sources.append (local_dest_file)

	 			working_dir = os.getcwd ()
				try:
					checkout (self, source, local_dest_file, workspace)
				except Exception as e:
					if os.path.exists(local_dest_file):
						print 'Deleting ' + local_dest_file + ' cache due to git error'
						shutil.rmtree(local_dest_file, ignore_errors=True)
					if os.path.exists(workspace):
						print 'Deleting ' + workspace + ' cache due to git error'
						shutil.rmtree(workspace, ignore_errors=True)

					# Explicitly reset the working dir to a known directory which has not been deleted
					# 'git clone' does not work if you are in a directory which has been deleted
					os.chdir (working_dir)
					checkout (self, source, local_dest_file, workspace)
				finally:
					os.chdir (workspace)
			else:
				raise Exception ('missing source: %s' % source)

		self.sources = local_sources

	def sources_dir (self):
		if not self._sources_dir:
			source_cache = os.getenv('BOCKBUILD_SOURCE_CACHE')
			self._sources_dir = source_cache or os.path.realpath (os.path.join (self.package_dir(), "..", "cache"))
		if not os.path.exists(self._sources_dir): os.mkdir (self._sources_dir)
		return self._sources_dir

	def package_dir (self):
		if not self._package_dir:
			self._package_dir = os.path.dirname (os.path.realpath (self._path))
		return self._package_dir

	def package_build_dir(self):
		return Package.profile.build_root

	def is_successful_build(self, build_success_file, package_dir):
		def is_newer(success_file):
			mtime = os.path.getmtime(success_file)
			for s in self.sources:
				src = os.path.join(package_dir, s)
				if os.path.isfile(src) and os.path.getmtime(src) > mtime:
						return False
			return True

		return os.path.exists (build_success_file) and is_newer(build_success_file)

	def delete_stale_workspace_cache (self, dirname):
		origin = backtick ('git --git-dir="%s" config --get remote.origin.url' % os.path.join (dirname, ".git"))
		# Not pointing to a git repo
		if not origin:
			return False

		# Pointing to a non gitmirror repo
		if not "gitmirror" in origin[0]:
			print "Cache does not point to a gitmirror"
			# Delete the old cache as well
			if os.path.exists (origin[0]):
				print "Deleting old cache " + origin[0]
				shutil.rmtree (origin [0], ignore_errors = True)
			print "Deleting workspace " + dirname
			shutil.rmtree (dirname, ignore_errors = True)
			return True

		# Make sure gitmirror exists
		if os.path.isfile (origin[0]) and not os.path.exists (origin[0]):
			print "Cache does not exist"
			return True
		else:
			# origin and "gitmirror" in origin[0] and os.path.exists (origin[0])
			return False

	def get_timestamp (self):
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	def start_build (self):
		Package.last_instance = None

		# hack: we need to expand macros in fields, but not for self.configure.
		# if we expand self.configure now, we can't adjust the prefix for multiple builds
		# needed for lipoing
		temp = self.configure
		self.configure = ""
		expand_macros (self, self)
		self.configure = temp

		profile = Package.profile
		namever = '%s-%s' % (self.name, self.version)
		package_dir = self.package_dir ()
		package_build_dir = self.package_build_dir()
		workspace = os.path.join (profile.build_root, namever)
		build_success_file = os.path.join (profile.build_root, namever + '.success')
		install_success_file = os.path.join (profile.build_root, namever + '.install')
		sources_dir = self.sources_dir ()

		old_package_build_dir = os.path.join (workspace, '_build')
		if os.path.exists(old_package_build_dir):
			shutil.rmtree (os.path.join(profile.build_root, namever))

		if self.delete_stale_workspace_cache (workspace):
			if os.path.exists (build_success_file): os.remove (build_success_file)

		if self.is_successful_build(build_success_file, package_dir) and not self.needs_lipo: 
			print 'Skipping %s - already built' % namever
			if not os.path.exists (install_success_file):
				print '%s: Installing %s' % (self.get_timestamp (), namever)
				os.chdir (package_build_dir)
				self.cd ('%{source_dir_name}')
				self.install ()
				open (install_success_file, 'w').close ()
			return

		print '\n\n%s: Building %s on %s (%s CPU)' % (self.get_timestamp (), self.name, profile.host, profile.cpu_count)

		if not os.path.exists (profile.build_root) or \
			not os.path.isdir (profile.build_root):
			os.makedirs (profile.build_root, 0755)

		# shutil.rmtree (package_build_dir, ignore_errors = True)
		# os.makedirs (package_build_dir)

		self._fetch_sources (workspace, package_dir, sources_dir)

		os.chdir (package_build_dir)

		for phase in Package.profile.run_phases:
			log (0, '%s: %sing %s' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), phase.capitalize (), self.name))
			getattr (self, phase) ()

		open (build_success_file, 'w').close ()
		open (install_success_file, 'w').close ()

	def sh (self, *commands):
		for command in commands:
			command = expand_macros (command, self)
			log (1, command)
			if not Package.profile.verbose:
				command = '( %s ) > /dev/null 2>&1' % command
			run_shell (command)

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
		if self.sources == None:
			log (1, '<skipping - no sources defined>')
			return

		if self.sources[0].endswith ('.gitmirror'):
			namever = '%s-%s' % (self.name, self.version)
			os.chdir (os.path.join (os.getcwd (), namever))
		else:
			self.extract_archive (self.sources[0], False)
			self.cd ('%{source_dir_name}')

	def extract_archive (self, local_dest_file, validate_only, overwrite=False):
		self.tar = os.path.join (Package.profile.prefix, 'bin', 'tar')
		if not os.path.exists (self.tar):
			self.tar = 'tar'
		root, ext = os.path.splitext (local_dest_file)
		command = None
		if ext == '.zip':
			flags = ["-qq"]
			if overwrite:
				flags.extend(["-o"])
			if validate_only:
				flags.extend(["-t"])
			command = ' '.join(['unzip'] + flags + [local_dest_file])
			if validate_only:
				command = command + ' > /dev/null'
		else:
			command = '%{tar} xf ' + local_dest_file
			if validate_only:
				command = command + ' -O > /dev/null'
		self.sh (command)

	def build (self):
		self.package_prefix = self.prefix
		if self.profile.name == 'darwin':
			if self.m64:
				if self.needs_lipo:
					log (1, 'Lipo (universal binaries) mode enabled.')	
					self.bin64_prefix = self.prefix  + '-darwin-64' #switch to a temporary prefix 
					self.package_prefix = self.bin64_prefix
					log (1, 'Building 64-bit binaries at ' + self.package_prefix)
					self.arch_build ('darwin-64')
					self.sh ('%{makeinstall}')
					self.sh ('%{make} clean')

					self.package_prefix = self.prefix #switch back to main prefix
					log (1, 'Building 32-bit binaries at ' + self.package_prefix)
					self.arch_build ('darwin-32')

				elif self.fat_build:
					log (1, 'Building 32/64-bit binaries at ' + self.package_prefix)
					self.arch_build ('darwin-fat')
				elif self.m32_only:
					self.arch_build ('darwin-32')
				elif self.build_dependency: # build dependencies can be built in the default architecture if not otherwise specified
					self.arch_build ('darwin-64')
				else:
					log (1, 'Building 32/64-bit binaries (default settings) at ' + self.package_prefix)
					self.arch_build ('darwin-fat')

			else:	
				self.arch_build ('darwin-32')
		else:
			self.arch_build (self.profile.name)

	def lipo_dirs (self, dir_64, dir_32, lipo_dir, bin_subdir, replace_32 = True): 
		dir64_bin = os.path.join (dir_64, bin_subdir)
		dir32_bin = os.path.join (dir_32, bin_subdir)
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

						lipo_cmd = 'lipo -create %s %s -output %s ' % (dir64_file, dir32_file, lipo_file) 
						#print lipo_cmd
						run_shell(lipo_cmd)
						if replace_32:
							#replace all 32-bit binaries with the new fat binaries
							shutil.copy2 (lipo_file, dir32_file)
					else:
						print "lipo warning: 32-bit version of file %s not found"  %file

			
	def arch_build (self, arch, defaults = True):
		if self.sources == None:
			log (1, '<skipping - no sources defined>')
			return

		if defaults: #the package does not define the strategy for buildling lipos. These are the defaults
			if (arch == 'darwin-fat'):					
					self.local_ld_flags = ['-arch i386' , '-arch x86_64']
					self.local_gcc_flags = ['-arch i386' , '-arch x86_64']
					self.local_configure_flags = ['--disable-dependency-tracking']
			elif (arch == 'darwin-32'):
					self.local_ld_flags = ['-arch i386']
					self.local_gcc_flags = ['-arch i386']
					self.local_configure_flags = ['--disable-dependency-tracking']
			elif (arch == 'darwin-64'):
					self.local_ld_flags = ['-arch x86_64']
					self.local_gcc_flags = ['-arch x86_64']
					self.local_configure_flags = ['--disable-dependency-tracking']

		Package.configure (self)
		Package.make (self)

	def configure (self):
		self.sh ('CXXFLAGS="%{gcc_flags} %{local_gcc_flags}" OBJCFLAGS="%{gcc_flags} %{local_gcc_flags}" CFLAGS="%{gcc_flags} %{local_gcc_flags}" CXXFLAGS="%{gcc_flags} %{local_gcc_flags}" CPPFLAGS="%{cpp_flags} %{local_cpp_flags}" LDFLAGS="%{ld_flags} %{local_ld_flags}" %{configure} %{configure_flags} %{local_configure_flags}')

	def make (self):
		self.sh ('%{make}')

	def install (self):
		if self.sources == None:
			log (1, '<skipping - no sources defined>')
			return
		self.sh ('%{makeinstall}')

		if self.needs_lipo: #lipo here
			lipo_dir = self.prefix + '-lipo'

			if not os.path.exists(lipo_dir):
				os.mkdir (lipo_dir)

			log (1, 'Lipoing binaries (lib)' + self.prefix)
			self.lipo_dirs (self.bin64_prefix, self.prefix, lipo_dir, 'lib')
			log (1, 'Lipoing binaries (bin)' + self.prefix)
			self.lipo_dirs (self.bin64_prefix, self.prefix, lipo_dir, 'bin')

			#delete the lipo build dirs
			shutil.rmtree (lipo_dir, ignore_errors = True)
			shutil.rmtree (self.bin64_prefix, ignore_errors = True)

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
			configure = './autogen.sh --prefix="%{prefix}"',
			configure_flags = configure_flags,
			sources = sources,
			override_properties = override_properties,
			revision = revision)

GnomeGitPackage.default_sources = [
	'git://git.gnome.org/%{name}'
]

class GnuPackage (Package): pass
GnuPackage.default_sources = [
	'http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz'
]

class GnuBz2Package (Package): pass
GnuBz2Package.default_sources = [
	'http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2'
]

class GnuXzPackage (Package): pass
GnuXzPackage.default_sources = [
        'http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz'
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
	'http://downloads.sourceforge.net/sourceforge/%{project}/%{name}-%{version}.tar.gz'
]

class FreeDesktopPackage (ProjectPackage): pass
FreeDesktopPackage.default_sources = [
	'http://%{project}.freedesktop.org/releases/%{name}-%{version}.tar.gz'
]

class GitHubTarballPackage (Package):
	def __init__ (self, org, name, version, commit, configure, override_properties = None):
		self.commit = commit
		self.org = org
		Package.__init__ (self, name, version,
			override_properties = override_properties)
		self.configure = configure
		self.source_dir_name = '%s-%s-%s' % ( org, name, self.commit[:7] )
GitHubTarballPackage.default_sources = [
	'http://github.com/%{org}/%{name}/tarball/%{commit}'
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
			
		profile = Package.profile
		namever = '%s-%s' % (self.name, self.version)
			
		self.revision_file = os.path.join (profile.build_root, namever + '.revision')
		
	def is_successful_build(self, build_success_file, package_dir):
		if not Package.is_successful_build(self, build_success_file, package_dir):
			return False
		return self.check_version_hash ()
			
	def check_version_hash (self):
		if os.path.isfile (self.revision_file):
			f = open (self.revision_file, 'r')
			check = f.readline ().strip ('\n')
			if check == self.revision:
				return True
		self.create_version_hash ()
		return False
		
	def create_version_hash (self):
		f = open (self.revision_file, 'w')
		f.write (self.revision)
		f.write ('\n')
		f.close()


class GstreamerPackage (ProjectPackage): pass
GstreamerPackage.default_sources = [
	'http://%{project}.freedesktop.org/src/%{name}/%{name}-%{version}.tar.gz'
]

class XiphPackage (ProjectPackage): pass
XiphPackage.default_sources = [
	'http://downloads.xiph.org/releases/%{project}/%{name}-%{version}.tar.gz'
]
