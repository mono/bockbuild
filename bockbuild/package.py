import os
import sys
import shutil
from urllib import FancyURLopener
from util import *

class Package:
	def __init__ (self, name, version, configure_flags = None, sources = None, source_dir_name = None, override_properties = None):
		Package.last_instance = self
		
		self._dirstack = []

		self.name = name
		self.version = version

		self.configure_flags = []
		if Package.profile.global_configure_flags:
			self.configure_flags.extend (Package.profile.global_configure_flags)
		if configure_flags:
			self.configure_flags.extend (configure_flags)

		self.sources = sources
		if self.sources == None \
			and not self.__class__.default_sources == None:
			self.sources = list (self.__class__.default_sources)

		self.source_dir_name = source_dir_name
		if self.source_dir_name == None:
			self.source_dir_name = '%{name}-%{version}'

		self.prefix = Package.profile.prefix
		self.configure = './configure --prefix="%{prefix}"'
		self.make = 'make -j%s' % Package.profile.cpu_count
		self.makeinstall = 'make install'
		self.git = 'git'
		for git in ['/usr/bin/git', '/usr/local/bin/git', '/usr/local/git/bin/git']:
			if os.path.isfile (git):
				self.git = git
				break

		if not override_properties == None:
			for k, v in override_properties.iteritems ():
				self.__dict__[k] = v

	def _fetch_sources (self, package_dir, package_dest_dir):
		if self.sources == None:
			return

		local_sources = []
		for source in self.sources:
			local_source = os.path.join (package_dir, source)
			local_source_file = os.path.basename (local_source)
			local_dest_file = os.path.join (package_dest_dir, local_source_file)
			local_sources.append (local_dest_file)
			
			if os.path.isfile (local_dest_file):
				log (1, 'using cached source: %s' % local_dest_file)
			elif os.path.isfile (local_source):
				log (1, 'copying local source: %s' % local_source_file)
				shutil.copy2 (local_source, local_dest_file)
			elif source.startswith (('http://', 'https://', 'ftp://')):
				log (1, 'downloading remote source: %s' % source)
				FancyURLopener ().retrieve (source, local_dest_file)
			elif source.startswith ('git://'):
				log (1, 'cloning or updating git repository: %s' % source)
				local_dest_file = os.path.join (package_dest_dir,
					'%s-%s.git' % (self.name, self.version))
				local_sources.pop ()
				local_sources.append (local_dest_file)
				pwd = os.getcwd ()
				if not os.path.isdir (os.path.join (local_dest_file, '.git')):
					self.cd (os.path.dirname (local_dest_file))
					shutil.rmtree (local_dest_file, ignore_errors = True)
					self.sh ('%' + '{git} clone "%s" "%s"' % (source, os.path.basename (local_dest_file)))
				else:
					self.cd (local_dest_file)
					self.sh ('%{git} pull --rebase')
				os.chdir (pwd)

		self.sources = local_sources

	def start_build (self):
		Package.last_instance = None
		
		expand_macros (self, self)

		profile = Package.profile

		namever = '%s-%s' % (self.name, self.version)
		package_dir = os.path.dirname (os.path.realpath (self._path))
		package_dest_dir = os.path.join (profile.build_root, namever)
		package_build_dir = os.path.join (package_dest_dir, '_build')
		build_success_file = os.path.join (profile.build_root,
			namever + '.success')

		if os.path.exists (build_success_file):
			print 'Skipping %s - already built' % namever
			return

		print '\n\nBuilding %s on %s (%s CPU)' % (self.name, profile.host,
			profile.cpu_count)

		if not os.path.exists (profile.build_root) or \
			not os.path.isdir (profile.build_root):
			os.makedirs (profile.build_root, 0755)

		shutil.rmtree (package_build_dir, ignore_errors = True)
		os.makedirs (package_build_dir)

		self._fetch_sources (package_dir, package_dest_dir)

		os.chdir (package_build_dir)

		for phase in Package.profile.run_phases:
			log (0, '%sing %s' % (phase.capitalize (), self.name))
			getattr (self, phase) ()

		open (build_success_file, 'w').close ()

	def sh (self, *commands):
		for command in commands:
			command = expand_macros (command, self)
			log (1, command)
			if not Package.profile.verbose:
				command = '( %s ) &>/dev/null' % command
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
		self.tar = os.path.join (Package.profile.prefix, 'bin', 'tar')
		if not os.path.exists (self.tar):
			self.tar = 'tar'

		if self.sources == None:
			log (1, '<skipping - no sources defined>')
			return

		if os.path.isdir (os.path.join (self.sources[0], '.git')):
			dirname = os.path.join (os.getcwd (), os.path.basename (self.sources[0]))
			self.sh ('cp -a "%s" "%s"' % (self.sources[0], dirname))
			self.cd (dirname)
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

class GnuPackage (Package): pass
GnuPackage.default_sources = [
	'http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz'
]

class GnuBz2Package (Package): pass
GnuBz2Package.default_sources = [
	'http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2'
]

class CairoGraphicsPackage (Package): pass
CairoGraphicsPackage.default_sources = [
	'http://cairographics.org/releases/%{name}-%{version}.tar.gz'
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

class GstreamerPackage (ProjectPackage): pass
GstreamerPackage.default_sources = [
	'http://%{project}.freedesktop.org/src/%{name}/%{name}-%{version}.tar.gz'
]

class XiphPackage (ProjectPackage): pass
XiphPackage.default_sources = [
	'http://downloads.xiph.org/releases/%{project}/%{name}-%{version}.tar.gz'
]
