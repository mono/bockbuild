import os
import shutil
from plistlib import Plist
from util.util import *
from unixprofile import UnixProfile

class DarwinProfile (UnixProfile):
	def __init__ (self, prefix = None, m64 = False, min_version = 6):
		UnixProfile.__init__ (self, prefix)
		
		self.name = 'darwin'
		self.m64 = m64

		if os.path.exists (self.prefix):
			error ('Prefix %s exists, and may interfere with the staged build. Please remove and try again.' % self.prefix)

		sdkroot = '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/'
		if (not os.path.isdir (sdkroot)):
			sdkroot = '/Developer/SDKs/'

		sdk_paths = (sdkroot + 'MacOSX10.%s.sdk' % v for v in range (min_version, 20)) #future-proof! :P

		for sdk in sdk_paths:
			if os.path.isdir (sdk):
				self.mac_sdk_path = sdk
				break

		if self.mac_sdk_path is None: error ('Mac OS X SDK (>=10.%s) not found under %s' % (min_version, sdkroot))

		self.gcc_flags.extend ([
				'-D_XOPEN_SOURCE',
				'-isysroot %s' % self.mac_sdk_path,
				'-Wl,-headerpad_max_install_names' #needed to ensure install_name_tool can succeed staging binaries
			])

		self.ld_flags.extend ([
				'-headerpad_max_install_names' #needed to ensure install_name_tool can succeed staging binaries
			])

		self.target_osx = '10.%s' % min_version

		if min_version:
			self.gcc_flags.extend (['-mmacosx-version-min=%s' % self.target_osx])
			self.env.set ('MACOSX_DEPLOYMENT_TARGET', self.target_osx)
		
		if self.cmd_options.debug is True:
			self.gcc_flags.extend ('-O0', '-ggdb3')

		if os.getenv('BOCKBUILD_USE_CCACHE') is None:
			self.env.set ('CC',  'xcrun gcc')
			self.env.set ('CXX', 'xcrun g++')
		else:
			self.env.set ('CC',  'ccache xcrun gcc')
			self.env.set ('CXX', 'ccache xcrun g++')

		self.staged_binaries = []
		self.staged_textfiles = []

		if self.arch == 'default':
			self.arch = 'darwin-32'

		# GTK2_RC_FILES must be a ":"-seperated list of files (NOT a single folder)
		self.gtk2_rc_files = os.path.join (os.getcwd (), 'skeleton.darwin', 'Contents', 'Resources', 'etc', 'gtk-2.0', 'gtkrc')
		self.env.set ('GTK2_RC_FILES', '%{gtk2_rc_files}')

	
	def arch_build (self, arch, package):
		if arch == 'darwin-universal':
			package.local_ld_flags = ['-arch i386' , '-arch x86_64']
			package.local_gcc_flags = ['-arch i386' , '-arch x86_64']
		elif arch == 'darwin-32':
			package.local_ld_flags = ['-arch i386','-m32']
			package.local_gcc_flags = ['-arch i386','-m32']
			package.local_configure_flags = ['--build=i386-apple-darwin11.2.0', '--disable-dependency-tracking']
		elif arch == 'darwin-64':
			package.local_ld_flags = ['-arch x86_64 -m64']
			package.local_gcc_flags = ['-arch x86_64 -m64']
			package.local_configure_flags = ['--disable-dependency-tracking']
		else:
			error ('Unknown arch %s' % arch)

		package.local_configure_flags.extend (['--cache-file=%s/%s-%s.cache' % (self.build_root, package.name, arch)])

	def bundle (self):
		self.make_app_bundle ()

	def make_app_bundle (self):
		plist_path = os.path.join (self.bundle_skeleton_dir, 'Contents', 'Info.plist')
		app_name = 'Unknown'
		plist = None
		if os.path.exists (plist_path):
			plist = Plist.fromFile (plist_path)
			app_name = plist['CFBundleExecutable']
		else:
			print 'Warning: no Contents/Info.plist in .app skeleton'

		self.bundle_app_dir = os.path.join (self.bundle_output_dir, app_name + '.app')
		self.bundle_contents_dir = os.path.join (self.bundle_app_dir, 'Contents')
		self.bundle_res_dir = os.path.join (self.bundle_contents_dir, 'Resources')
		self.bundle_macos_dir = os.path.join (self.bundle_contents_dir, 'MacOS')

		# Create the .app tree, copying the skeleton
		shutil.rmtree (self.bundle_app_dir, ignore_errors = True)
		shutil.copytree (self.bundle_skeleton_dir, self.bundle_app_dir)
		if not os.path.exists (self.bundle_contents_dir): os.makedirs (self.bundle_contents_dir)
		if not os.path.exists (self.bundle_res_dir): os.makedirs (self.bundle_res_dir)
		if not os.path.exists (self.bundle_macos_dir): os.makedirs (self.bundle_macos_dir)

		# Generate the PkgInfo
		pkginfo_path = os.path.join (self.bundle_contents_dir, 'PkgInfo')
		if not os.path.exists (pkginfo_path) and not plist == None:
			fp = open (pkginfo_path, 'w')
			fp.write (plist['CFBundlePackageType'])
			fp.write (plist['CFBundleSignature'])
			fp.close ()

		# Run solitary against the installation to collect files
		files = ''
		for file in self.bundle_from_build:
			files = files + ' "%s"' % os.path.join (self.prefix, file)

		run_shell ('mono --debug ../../solitary/Solitary.exe '
			'--mono-prefix="%s" --root="%s" --out="%s" %s' % \
			(self.prefix, self.prefix, self.bundle_res_dir, files))
		self.configure_gtk ()
		self.configure_gdk_pixbuf ()

	def configure_gtk (self):
		paths = [
			os.path.join ('etc', 'gtk-2.0', 'gtk.immodules'),
			os.path.join ('etc', 'gtk-2.0', 'im-multipress.conf'),
			os.path.join ('etc', 'pango', 'pango.modules')
		]

		for path in paths:
			bundle_path = os.path.join (self.bundle_res_dir, path) + '.in'
			path = os.path.join (self.prefix, path)

			if not os.path.isfile (path):
				continue

			try:
				os.makedirs (os.path.dirname (bundle_path))
			except:
				pass

			ifp = open (path)
			ofp = open (bundle_path, 'w')
			for line in ifp:
				if line.startswith ('#'):
					continue
				ofp.write (line.replace (self.prefix, '${APP_RESOURCES}'))
			ifp.close ()
			ofp.close ()

			if os.path.basename (path) == 'pango.modules':
				fp = open (os.path.join (os.path.dirname (bundle_path), 'pangorc'), 'w')
				fp.write ('[Pango]\n')
				fp.write ('ModuleFiles=./pango.modules\n')
				fp.close ()

	def configure_gdk_pixbuf (self):
		path = os.path.join (self.bundle_res_dir, 'etc', 'gtk-2.0', 'gdk-pixbuf.loaders.in')

		# HACK solitary relocates some .dylib so that gdk-pixbuf-query-loaders will fail
		# if not run from the build-root/_install/lib/ directory
		os.chdir ('%s/lib/' % self.prefix)

		run_shell ('gdk-pixbuf-query-loaders 2>/dev/null | ' + \
			'sed \'s,%s,\\${APP_RESOURCES},g\' 1> "%s"' % (self.prefix, path))
