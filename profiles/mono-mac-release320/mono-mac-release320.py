#!/usr/bin/python -B -u

import itertools
import os
import re
import shutil
import string
import sys
import tempfile

sys.path.append('../..')

from bockbuild.darwinprofile import DarwinProfile
from bockbuild.util.util import *
from packages import MonoReleasePackages
from glob import glob


class MonoReleaseProfile(DarwinProfile, MonoReleasePackages):
    def __init__(self):
        self.MONO_ROOT = "/Library/Frameworks/Mono.framework"
        self.RELEASE_VERSION = os.getenv('MONO_VERSION')
        self.BUILD_NUMBER = "0"
        self.MRE_GUID = "432959f9-ce1b-47a7-94d3-eb99cb2e1aa8"
        self.MDK_GUID = "964ebddd-1ffe-47e7-8128-5ce17ffffb05"

        if self.RELEASE_VERSION is None:
            raise Exception("Please define the environment variable: MONO_VERSION")

        # Create the updateid
        parts = self.RELEASE_VERSION.split(".")
        version_list = (parts + ["0"] * (3 - len(parts)))[:4]
        for i in range(1, 3):
            version_list[i] = version_list[i].zfill(2)
            self.updateid = "".join(version_list)
            self.updateid += self.BUILD_NUMBER.replace(".", "").zfill(9 - len(self.updateid))

        versions_root = os.path.join(self.MONO_ROOT, "Versions")
        self.release_root = os.path.join(versions_root, self.RELEASE_VERSION)

        DarwinProfile.__init__(self, self.release_root)
        MonoReleasePackages.__init__(self)

        self.self_dir = os.path.realpath(os.path.dirname(sys.argv[0]))
        self.packaging_dir = os.path.join(self.self_dir, "packaging")

        aclocal_dir = os.path.join(self.prefix, "share", "aclocal")
        if not os.path.exists(aclocal_dir):
            os.makedirs(aclocal_dir)

    def build(self):
        if not os.path.exists(os.path.join(self.release_root, "bin")):
            log(0, "Rebuilding world - new prefix: " + self.release_root)
            shutil.rmtree(self.build_root, ignore_errors=True)
        DarwinProfile.build(self)

    def make_package_symlinks(self, root):
        os.symlink(self.prefix, os.path.join(root, "Versions", "Current"))
        currentlink = os.path.join(self.MONO_ROOT, "Versions", "Current")
        links = [
            ("bin", "Commands"),
            ("include", "Headers"),
            ("lib", "Libraries"),
            ("", "Home"),
            (os.path.join("lib", "libmono-2.0.dylib"), "Mono")
        ]
        for srcname, destname in links:
            src = os.path.join(currentlink, srcname)
            dest = os.path.join(root, destname)
            #If the symlink exists, we remove it so we can create a fresh one
            if os.path.exists(dest):
                os.unlink(dest)
            os.symlink(src, dest)

    # creates and returns the path to a working directory containing:
    #   PKGROOT/ - this root will be bundled into the .pkg and extracted at /
    #   uninstallMono.sh - copied onto the DMG
    #   Info{_sdk}.plist - used by packagemaker to make the installer
    #   resources/ - other resources used by packagemaker for the installer
    def setup_working_dir(self):
        tmpdir = tempfile.mkdtemp()
        monoroot = os.path.join(tmpdir, "PKGROOT", self.MONO_ROOT[1:])
        versions = os.path.join(monoroot, "Versions")
        pcl_assemblies = os.path.join(monoroot, "External", "xbuild-frameworks", ".NETPortable")
        os.makedirs(versions)
        os.makedirs(pcl_assemblies)

        print "setup_working_dir " + tmpdir
        # setup metadata
        backtick('rsync -aP %s/* %s' % (self.packaging_dir, tmpdir))
        parameter_map = {
            '@@MONO_VERSION@@': self.RELEASE_VERSION,
            '@@MONO_RELEASE@@': self.BUILD_NUMBER,
            '@@MONO_VERSION_RELEASE@@': self.RELEASE_VERSION + '_' + self.BUILD_NUMBER,
            '@@MONO_PACKAGE_GUID@@': self.MRE_GUID,
            '@@MONO_CSDK_GUID@@': self.MDK_GUID,
            '@@MONO_VERSION_RELEASE_INT@@': self.updateid,
            '@@PACKAGES@@': string.join(set([root for root, ext in map(os.path.splitext, os.listdir(self.build_root))]), "\\\n"),
            '@@DEP_PACKAGES@@': ""
        }
        for dirpath, d, files in os.walk(tmpdir):
            for name in files:
                if not name.startswith('.'):
                    replace_in_file(os.path.join(dirpath, name), parameter_map)

        self.make_package_symlinks(monoroot)

        # copy to package root
        backtick('rsync -aP "%s" "%s"' % (self.release_root, versions))

        # copy pcl assemblies
        pcl_root = os.path.join(self.MONO_ROOT, "External", "xbuild-frameworks", ".NETPortable")
        backtick('rsync -aP "%s/" "%s"' % (pcl_root, pcl_assemblies))

        return tmpdir

    def apply_blacklist(self, working_dir, blacklist_name):
        blacklist = os.path.join(working_dir, blacklist_name)
        root = os.path.join(working_dir, "PKGROOT", self.release_root[1:])
        backtick(blacklist + ' "%s"' % root)

    def run_pkgbuild(self, working_dir, package_type):
        info = self.package_info(package_type)
        output = os.path.join(self.self_dir, info["filename"])
        identifier = "com.xamarin.mono-" + info["type"] + ".pkg"
        resources_dir = os.path.join(working_dir, "resources")
        distribution_xml = os.path.join(resources_dir, "distribution.xml")

        old_cwd = os.getcwd()
        os.chdir(working_dir)
        pkgbuild = "/usr/bin/pkgbuild"
        pkgbuild_cmd = ' '.join([pkgbuild,
                                 "--identifier " + identifier,
                                 "--root '%s/PKGROOT'" % working_dir,
                                 "--version '%s'" % self.RELEASE_VERSION,
                                 "--install-location '/'",
                                 "--scripts '%s'" % resources_dir,
                                 os.path.join(working_dir, "mono.pkg")])
        print pkgbuild_cmd
        backtick(pkgbuild_cmd)

        productbuild = "/usr/bin/productbuild"
        productbuild_cmd = ' '.join([productbuild,
                                     "--resources %s" % resources_dir,
                                     "--distribution %s" % distribution_xml,
                                     "--package-path %s" % working_dir,
                                     output])
        print productbuild_cmd
        backtick(productbuild_cmd)
        os.chdir(old_cwd)
        return output

    def make_updateinfo(self, working_dir, guid):
        updateinfo = os.path.join(
            working_dir, "PKGROOT", self.release_root[1:], "updateinfo")
        with open(updateinfo, "w") as updateinfo:
            updateinfo.write(guid + ' ' + self.updateid + "\n")

    def package_info(self, pkg_type):
        version = self.RELEASE_VERSION
        info = (pkg_type, version)
        filename = "MonoFramework-%s-%s.macos10.xamarin.x86.pkg" % info
        return {
            "type": pkg_type,
            "filename": filename,
            "title": "Mono Framework %s %s " % info
        }

    def build_package(self):
        working = self.setup_working_dir()
        uninstall_script = os.path.join(working, "uninstallMono.sh")

        # make the MDK
        self.apply_blacklist(working, 'mdk_blacklist.sh')
        self.make_updateinfo(working, self.MDK_GUID)
        mdk_pkg = self.run_pkgbuild(working, "MDK")
        print "Saving: " + mdk_pkg
        # self.make_dmg(mdk_dmg, title, mdk_pkg, uninstall_script)

        # make the MRE
        self.apply_blacklist(working, 'mre_blacklist.sh')
        self.make_updateinfo(working, self.MRE_GUID)
        mre_pkg = self.run_pkgbuild(working, "MRE")
        print "Saving: " + mre_pkg
        # self.make_dmg(mre_dmg, title, mre_pkg, uninstall_script)

        shutil.rmtree(working)

    def generate_dsym(self):
        for path, dirs, files in os.walk(self.prefix):
            for name in files:
                f = os.path.join(path, name)
                file_type = backtick('file "%s"' % f)
                if "dSYM" in f:
                    continue
                if "Mach-O" in "".join(file_type):
                    print "Generating dsyms for %s" % f
                    backtick('dsymutil "%s"' % f)

    def install_root(self):
        return os.path.join(self.MONO_ROOT, "Versions", self.RELEASE_VERSION)

    def fix_line(self, line, matcher):
        def insert_install_root(matches):
            root = self.install_root()
            captures = matches.groupdict()
            return 'target="%s"' % os.path.join(root, "lib", captures["lib"])

        if matcher(line):
            pattern = r'target="(?P<lib>.+\.dylib)"'
            result = re.sub(pattern, insert_install_root, line)
            return result
        else:
            return line

    def fix_dllmap(self, config, matcher):
        handle, temp = tempfile.mkstemp()
        with open(config) as c:
            with open(temp, "w") as output:
                for line in c:
                    output.write(self.fix_line(line, matcher))
        os.rename(temp, config)
        os.system('chmod a+r %s' % config)

    def fix_libMonoPosixHelper(self):
        config = os.path.join(self.prefix, "etc", "mono", "config")
        self.fix_dllmap(
            config, lambda line: "libMonoPosixHelper.dylib" in line)

    def fix_gtksharp_configs(self):
        libs = [
            'atk-sharp',
            'gdk-sharp',
            'glade-sharp',
            'glib-sharp',
            'gtk-dotnet',
            'gtk-sharp',
            'pango-sharp'
        ]
        gac = os.path.join(self.install_root(), "lib", "mono", "gac")
        confs = [glob(os.path.join(gac, x, "*", "*.dll.config")) for x in libs]
        for c in itertools.chain(*confs):
            print "Fixing up " + c
            self.fix_dllmap(c, lambda line: "dllmap" in line)

    # THIS IS THE MAIN METHOD FOR MAKING A PACKAGE
    def package(self):
        self.fix_libMonoPosixHelper()
        self.fix_gtksharp_configs()
        self.generate_dsym()
        blacklist = os.path.join(self.packaging_dir, 'mdk_blacklist.sh')
        backtick(blacklist + ' ' + self.release_root)
        self.build_package()

MonoReleaseProfile().build()

profname = "mono-mac-release-env"
dir = os.path.realpath(os.path.dirname(sys.argv[0]))
envscript = '''#!/bin/sh
PROFNAME="%s"
INSTALLDIR=%s/build-root/_install
export DYLD_FALLBACK_LIBRARY_PATH="$INSTALLDIR/lib:/lib:/usr/lib:$DYLD_FALLBACK_LIBRARY_PATH"
export C_INCLUDE_PATH="$INSTALLDIR/include:$C_INCLUDE_PATH"
export ACLOCAL_PATH="$INSTALLDIR/share/aclocal:$ACLOCAL_PATH"
export ACLOCAL_FLAGS="-I $INSTALLDIR/share/aclocal $ACLOCAL_FLAGS"
export PKG_CONFIG_PATH="$INSTALLDIR/lib/pkgconfig:$INSTALLDIR/lib64/pkgconfig:$INSTALLDIR/share/pkgconfig:$PKG_CONFIG_PATH"
export CONFIG_SITE="$INSTALLDIR/$PROFNAME-config.site"
export MONO_GAC_PREFIX="$INSTALLDIR:MONO_GAC_PREFIX"
export MONO_ADDINS_REGISTRY="$INSTALLDIR/addinreg"
export PATH="$INSTALLDIR/bin:$PATH"
export MONO_INSTALL_PREFIX="$INSTALLDIR"

#mkdir -p "$INSTALLDIR"
#echo "test \"\$prefix\" = NONE && prefix=\"$INSTALLDIR\"" > $CONFIG_SITE

PS1="[$PROFNAME] \w @ "
''' % (profname, dir)

with open(os.path.join(dir, profname), 'w') as f:
    f.write(envscript)
