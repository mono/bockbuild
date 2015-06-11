import itertools
import os
import re
import shutil
import string
import sys
import tempfile
import shutil
import stat

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
            raise Exception("You must export MONO_VERSION to use this build profile. e.g. export MONO_VERSION=1.0.0")

        versions_root = os.path.join(self.MONO_ROOT, "Versions")
        release_root = os.path.join(versions_root, self.RELEASE_VERSION)

        DarwinProfile.__init__(self, prefix = release_root, min_version = 7)
        MonoReleasePackages.__init__(self)

        self.self_dir = os.path.realpath(os.path.dirname(sys.argv[0]))
        self.packaging_dir = os.path.join(self.self_dir, "packaging")

        aclocal_dir = os.path.join(self.staged_prefix, "share", "aclocal")
        if not os.path.exists(aclocal_dir):
            os.makedirs(aclocal_dir)

        registry_dir = os.path.join(self.staged_prefix, "etc", "mono", "registry", "LocalMachine")
        if not os.path.exists(registry_dir):
            os.makedirs(registry_dir)

    def build(self):
        self.staged_binaries = []
        self.staged_textfiles = []
        DarwinProfile.build(self)

    # THIS IS THE MAIN METHOD FOR MAKING A PACKAGE
    def package(self):
        self.restore_binaries ()
        self.restore_textfiles ()
        self.fix_gtksharp_configs()
        self.generate_dsym()
        self.verify_binaries()

        working = self.setup_working_dir()
        uninstall_script = os.path.join(working, "uninstallMono.sh")

        # make the preinstall script
        self.make_preinstall(working);

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

    def calculate_updateid(self):
        # Create the updateid
        if os.getenv('BOCKBUILD_ADD_BUILD_NUMBER'):
            self.find_git()
            print "cur path is %s and git is %s" % (os.getcwd(), self.git)
            blame_rev_str = 'cd %s/mono; %s blame configure.ac HEAD | grep AC_INIT | sed \'s/ .*//\' ' % (self.build_root, self.git)
            print blame_rev_str
            blame_rev = backtick(blame_rev_str)
            print "Last commit to the version string %s" % (blame_rev)
            blame_rev = " ".join(blame_rev)
            version_number_str = 'cd %s/mono; %s log %s..HEAD --oneline | wc -l | sed \'s/ //g\'' % (self.build_root, self.git, blame_rev)
            print version_number_str
            build_number = backtick(version_number_str)
            print "Calculating commit distance, %s" % (build_number)
            self.BUILD_NUMBER = " ".join(build_number)
            self.FULL_VERSION = self.RELEASE_VERSION + "." + self.BUILD_NUMBER
        else:
            self.BUILD_NUMBER="0"
            self.FULL_VERSION = self.RELEASE_VERSION

        parts = self.RELEASE_VERSION.split(".")
        version_list = (parts + ["0"] * (3 - len(parts)))[:4]
        for i in range(1, 3):
            version_list[i] = version_list[i].zfill(2)
            self.updateid = "".join(version_list)
            self.updateid += self.BUILD_NUMBER.replace(".", "").zfill(9 - len(self.updateid))


    # creates and returns the path to a working directory containing:
    #   PKGROOT/ - this root will be bundled into the .pkg and extracted at /
    #   uninstallMono.sh - copied onto the DMG
    #   Info{_sdk}.plist - used by packagemaker to make the installer
    #   resources/ - other resources used by packagemaker for the installer
    def setup_working_dir(self):
        def make_package_symlinks(root):
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

        tmpdir = tempfile.mkdtemp()
        monoroot = os.path.join(tmpdir, "PKGROOT", self.MONO_ROOT[1:])
        versions = os.path.join(monoroot, "Versions")
        os.makedirs(versions)

        print "Setting up temporary package directory:", tmpdir

        self.calculate_updateid()

        # setup metadata
        run_shell('rsync -aPq %s/* %s' % (self.packaging_dir, tmpdir), False)

        packages_list = string.join([pkg.get_package_string () for pkg in self.release_packages], "\\\n")
        deps_list = 'bockbuild (rev. %s)\\\n' % self.bockbuild_revision + string.join([pkg.get_package_string () for pkg in self.toolchain_packages], "\\\n")

        parameter_map = {
            '@@MONO_VERSION@@': self.RELEASE_VERSION,
            '@@MONO_RELEASE@@': self.BUILD_NUMBER,
            '@@MONO_VERSION_RELEASE@@': self.RELEASE_VERSION + '_' + self.BUILD_NUMBER,
            '@@MONO_PACKAGE_GUID@@': self.MRE_GUID,
            '@@MONO_CSDK_GUID@@': self.MDK_GUID,
            '@@MONO_VERSION_RELEASE_INT@@': self.updateid,
            '@@PACKAGES@@': packages_list,
            '@@DEP_PACKAGES@@': deps_list
        }
        for dirpath, d, files in os.walk(tmpdir):
            for name in files:
                if not name.startswith('.'):
                    replace_in_file(os.path.join(dirpath, name), parameter_map)

        make_package_symlinks(monoroot)

        # copy to package root
        run_shell('rsync -aPq "%s" "%s"' % (self.staged_prefix, versions), False)

        return tmpdir

    def apply_blacklist(self, working_dir, blacklist_name):
        print "Applying blacklist script:", blacklist_name
        blacklist = os.path.join(self.packaging_dir, blacklist_name)
        root = os.path.join(working_dir, "PKGROOT", self.prefix[1:])
        run_shell('%s "%s" > /dev/null' % (blacklist, root), print_cmd = False)

    def make_preinstall(self, working_dir):
        print 'Interpolating scripts...',
        template_file = working_dir + "/preinstall.template"

        resources_dir = os.path.join(working_dir, "resources")
        preinstall_file = resources_dir + "/preinstall"

        shutil.move(template_file, preinstall_file)
        replace_in_file(preinstall_file, {"RELEASE_VERSION": self.RELEASE_VERSION})
        perms = os.stat(preinstall_file)
        os.chmod(preinstall_file, perms.st_mode | stat.S_IEXEC | stat.S_IWGRP | stat.S_IXOTH)


    def run_pkgbuild(self, working_dir, package_type):
        print 'Running pkgbuild & productbuild...',
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
                                 "--quiet",
                                 os.path.join(working_dir, "mono.pkg")])

        run_shell(pkgbuild_cmd)

        productbuild = "/usr/bin/productbuild"
        productbuild_cmd = ' '.join([productbuild,
                                     "--resources %s" % resources_dir,
                                     "--distribution %s" % distribution_xml,
                                     "--package-path %s" % working_dir,
                                     "--quiet",
                                     output])

        run_shell(productbuild_cmd)
        os.chdir(old_cwd)
        print output
        return output

    def make_updateinfo(self, working_dir, guid):
        updateinfo = os.path.join(
            working_dir, "PKGROOT", self.prefix[1:], "updateinfo")
        with open(updateinfo, "w") as updateinfo:
            updateinfo.write(guid + ' ' + self.updateid + "\n")

    def package_info(self, pkg_type):

        if self.arch == "darwin-32":
            arch_str = "x86"
        elif self.arch == "darwin-64":
            arch_str = "x64"
        elif self.arch == "darwin-universal":
            arch_str = "universal"

        info = (pkg_type, self.FULL_VERSION, arch_str)

        filename = "MonoFramework-%s-%s.macos10.xamarin.%s.pkg" % info
        return {
            "type": pkg_type,
            "filename": filename
        }

    def generate_dsym(self):
        print 'Generating dsyms...',
        x = 0
        for path, dirs, files in os.walk(self.staged_prefix):
            for name in files:
                f = os.path.join(path, name)
                file_type = backtick('file "%s"' % f)
                if "dSYM" in f:
                    continue
                if "Mach-O" in "".join(file_type):
                    try:
                        run_shell('dsymutil "%s" >/dev/null' % f)
                        x = x + 1
                    except Exception as e:
                        warn (e)
        print x

    def fix_line(self, line, matcher):
        def insert_install_root(matches):
            root = self.prefix
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

    def fix_gtksharp_configs(self):
        print 'Fixing GTK# configuration files...',
        count = 0
        libs = [
            'atk-sharp',
            'gdk-sharp',
            'glade-sharp',
            'glib-sharp',
            'gtk-dotnet',
            'gtk-sharp',
            'pango-sharp'
        ]
        gac = os.path.join(self.staged_prefix, "lib", "mono", "gac")
        confs = [glob(os.path.join(gac, x, "*", "*.dll.config")) for x in libs]
        for c in itertools.chain(*confs):
            count = count + 1
            self.fix_dllmap(c, lambda line: "dllmap" in line)
        print count

    def restore_binaries (self):
        print 'Unstaging binaries...',
        x = 0
        for staged_path in self.staged_binaries:
            final_path = staged_path.replace (self.staged_prefix, self.prefix)
            run_shell ('install_name_tool -id %s %s' % (final_path, staged_path ))
            libs = backtick ('otool -L %s' % staged_path)
            for line in libs:
                rpath = line.split(' ')[0]
                if rpath.find (self.staged_prefix) != -1:
                        remap = rpath.replace (self.staged_prefix,self.prefix)
                        run_shell ('install_name_tool -change %s %s %s' % (rpath, remap, staged_path))
            os.remove (staged_path + '.release')
            x = x + 1
        print x

    def unstage_textfile (self, staged_path):
        with open(staged_path) as text:
                output = open(staged_path + '.unstage', 'w')
                for line in text:
                    tokens = line.split (" ")
                    for idx,token in enumerate(tokens):
                        if  token.find (self.staged_prefix) != -1:
                            tokens[idx] = token.replace(self.staged_prefix,self.prefix)
                    output.write (" ".join(tokens))
                output.close
        shutil.move (staged_path + '.unstage', staged_path)
        os.chmod (staged_path, os.stat (staged_path + '.release').st_mode)
        os.remove (staged_path + '.release')

    def restore_textfiles (self):
        print 'Unstaging textfiles...',
        x = 0
        for staged_path in self.staged_textfiles:
            self.unstage_textfile (staged_path)
            x = x + 1

        # TODO: Deprecate profile.staged_textfiles since it ties bockbuild's Packaging phase
        # to the Build phase. Then, we can use this for the extra stage files:

        # for package in self.release_packages:
        #     for extra_file in package.extra_stage_files:
        #         print extra_file
        #         self.unstage_textfile (os.path.join (self.staged_prefix, extra_file))
        #         x = x + 1
        # print x

    def verify(self, f):
        result = " ".join(backtick("otool -L " + f))
        regex = os.path.join(self.MONO_ROOT, "Versions", r"(\d+\.\d+\.\d+)")
        match = re.search(regex, result).group(1)
        if self.RELEASE_VERSION not in match:
            raise Exception("%s references Mono %s\n%s" % (f, match, result))

    def verify_binaries(self):
        bindir = os.path.join(self.staged_prefix, "bin")
        for path, dirs, files in os.walk(bindir):
            for name in files:
                f = os.path.join(path, name)
                file_type = backtick('file "%s"' % f)
                if "Mach-O executable" in "".join(file_type):
                    self.verify(f)

def main():
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

if __name__ == "__main__":
    main()
