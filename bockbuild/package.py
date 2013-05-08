import hashlib
import os
import sys
import shutil
import tempfile
from urllib import FancyURLopener
from util.util import *

class Package:
	def __init__ (self, name, version, organization = None, configure_flags = None, sources = None, revision = None, git_branch = 'master', source_dir_name = None, override_properties = None, configure = None):
		Package.last_instance = self

		self._dirstack = []

		self.name = name
		self.version = version
		self.organization = organization

		self.configure_flags = []
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
			self.configure = './configure --prefix="%{prefix}"'

		self.make = 'make -j%s' % Package.profile.cpu_count
		self.makeinstall = 'make install'
		self.git = 'git'
		self.git_branch = git_branch
		for git in ['/usr/bin/git', '/usr/local/bin/git', '/usr/local/git/bin/git']:
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

	def _fetch_sources (self, package_dir, package_dest_dir):

		def get_local_filename(source):
			return source if os.path.isfile(source) else os.path.join (package_dest_dir, os.path.basename (source))

		def get_cache_name (name):
			if self.organization == None:
				return self.name
			else:
				return self.organization + "+" + name


		if self.sources == None:
			return

		if not os.path.exists (package_dest_dir):
			os.mkdir (package_dest_dir)

		local_sources = []
		for source in self.sources:
			local_source = os.path.join (package_dir, source)
			local_source_file = os.path.basename (local_source)
			local_dest_file = get_local_filename (local_source)
			local_sources.append (local_dest_file)

			if os.path.isfile(local_dest_file):
				log (1, 'using cached source: %s' % local_dest_file)
			elif os.path.isfile (local_source):
				log (1, 'copying local source: %s' % local_source_file)
				shutil.copy2 (local_source, local_dest_file)
			elif source.startswith (('http://', 'https://', 'ftp://')):
				log (1, 'downloading remote source: %s' % source)
				filename, message = FancyURLopener ().retrieve (source, local_dest_file)

			elif source.startswith (('git://','file://', 'ssh://')) or source.endswith ('.git'):
				log (1, 'cloning or updating git repository: %s' % source)
				local_name = os.path.splitext(os.path.basename(source))[0]
				local_dest_file = os.path.join (package_dest_dir, '%s.gitmirror' % (get_cache_name (local_name)))

				local_sources.pop ()
				local_sources.append (local_dest_file)
				pwd = os.getcwd ()
				if os.path.isdir (local_dest_file):
					self.cd (local_dest_file)
					self.sh ('%{git} fetch')
					self.sh ('%{git} remote prune origin')
				else:
					self.cd (os.path.dirname (local_dest_file))
					shutil.rmtree (local_dest_file, ignore_errors = True)
					self.sh ('%' + '{git} clone --mirror "%s" "%s"' % (source, os.path.basename (local_dest_file)))

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
		origin = backtick ("git --git-dir=%s config --get remote.origin.url" % os.path.join (dirname, ".git"))
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

	def start_build (self):
		Package.last_instance = None

		expand_macros (self, self)

		profile = Package.profile
		namever = '%s-%s' % (self.name, self.version)
		package_dir = self.package_dir ()
		package_build_dir = profile.build_root
		workspace = os.path.join (profile.build_root, namever)
		build_success_file = os.path.join (profile.build_root, namever + '.success')
		install_success_file = os.path.join (profile.build_root, namever + '.install')
		sources_dir = self.sources_dir ()

		old_package_build_dir = os.path.join (workspace, '_build')
		if os.path.exists(old_package_build_dir):
			shutil.rmtree (os.path.join(profile.build_root, namever))

		if self.delete_stale_workspace_cache (workspace):
			if os.path.exists (build_success_file): os.remove (build_success_file)

		if self.is_successful_build(build_success_file, package_dir):
			print 'Skipping %s - already built' % namever
			if not os.path.exists (install_success_file):
				print 'Installing %s' % namever
				os.chdir (package_build_dir)
				self.cd ('%{source_dir_name}')
				self.install ()
				open (install_success_file, 'w').close ()
			return

		print '\n\nBuilding %s on %s (%s CPU)' % (self.name, profile.host, profile.cpu_count)

		if not os.path.exists (profile.build_root) or \
			not os.path.isdir (profile.build_root):
			os.makedirs (profile.build_root, 0755)

		# shutil.rmtree (package_build_dir, ignore_errors = True)
		# os.makedirs (package_build_dir)

		self._fetch_sources (package_dir, sources_dir)

		os.chdir (package_build_dir)

		for phase in Package.profile.run_phases:
			log (0, '%sing %s' % (phase.capitalize (), self.name))
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

	def working_clone(self, dirname):
		if not os.path.exists(dirname):
			return False

		# Check to see if it has the right files for a bare repo
		for i in ['FETCH_HEAD', 'HEAD', 'config', 'objects', 'packed-refs', 'refs']:
			if not os.path.exists(os.path.join(dirname, i)): return False

		return True

	def prep (self):
		self.tar = os.path.join (Package.profile.prefix, 'bin', 'tar')
		if not os.path.exists (self.tar):
			self.tar = 'tar'

		if self.sources == None:
			log (1, '<skipping - no sources defined>')
			return

		if self.sources[0].endswith ('.gitmirror'):
			dirname = os.path.join (os.getcwd (), expand_macros ('%{name}-%{version}', self))
			# self.sh ('cp -a "%s" "%s"' % (self.sources[0], dirname))
			if not working_clone(dirname):
				if os.path.exists(dirname):
					os.rmtree(dirname)
				self.sh ('git clone --local --shared "%s" "%s"' % (self.sources[0], dirname))

			self.cd (dirname)
			self.sh ('git fetch')
			self.sh ('%{git} clean -xfd')

			self.sh ('%{git} reset --hard')

			if self.revision != None:
				self.sh ('%' + '{git} checkout %s' % self.revision)
			elif self.git_branch != None:
				self.sh ('%' + '{git} checkout origin/%s' % self.git_branch)
			else:
				self.sh ('%{git} checkout origin/master')

		else:
			root, ext = os.path.splitext (self.sources[0])
			if ext == '.zip':
				self.sh ('unzip -qq "%{sources[0]}"')
			else:
				self.sh ('%{tar} xf "%{sources[0]}"')
			self.cd ('%{source_dir_name}')

	def build (self):
		if self.sources == None:
			log (1, '<skipping - no sources defined>')
			return
		self.sh ('%{configure} %{configure_flags}')
		self.sh ('%{make}')

	def install (self):
		if self.sources == None:
			log (1, '<skipping - no sources defined>')
			return
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
	def __init__ (self, organization, name, version, revision = None, git_branch = None, configure_flags = None, override_properties = None):
		Package.__init__ (self, name, version,
			organization = organization,
			revision = revision,
			git_branch = git_branch,
			configure_flags = configure_flags,
			sources = ['git://github.com/%{organization}/%{name}.git'],
			override_properties = override_properties)

class GstreamerPackage (ProjectPackage): pass
GstreamerPackage.default_sources = [
	'http://%{project}.freedesktop.org/src/%{name}/%{name}-%{version}.tar.gz'
]

class XiphPackage (ProjectPackage): pass
XiphPackage.default_sources = [
	'http://downloads.xiph.org/releases/%{project}/%{name}-%{version}.tar.gz'
]
