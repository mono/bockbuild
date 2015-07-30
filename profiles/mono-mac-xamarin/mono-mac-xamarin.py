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

sys.path.append('../mono-mac-release')

from MonoReleaseProfile import MonoReleaseProfile

class MonoXamarinPackageProfile(MonoReleaseProfile, MonoReleasePackages):
    def __init__(self):
        MonoReleaseProfile.__init__ (self)
        if self.cmd_options.do_package:
            self.identity = "Developer ID Installer: Xamarin Inc"

            output = backtick("security -v find-identity")
            if self.identity not in " ".join(output):
                error ("Identity '%s' was not found" % self.identity)

            password = os.getenv("CODESIGN_KEYCHAIN_PASSWORD")
            if password:
                print "Unlocking the keychain"
                backtick("security unlock-keychain -p %s" % password)
            else:
                error ("CODESIGN_KEYCHAIN_PASSWORD needs to be defined")


    def run_pkgbuild(self, working_dir, package_type):
        info = self.package_info(package_type)
        output = os.path.join(self.self_dir, info["filename"])
        temp = os.path.join(self.self_dir, "mono-%s.pkg" % package_type)
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
                                 # "--sign '%s'" % identity,
                                 "--scripts '%s'" % resources_dir,
                                 "--quiet",
                                 os.path.join(working_dir, "mono.pkg")])
        print pkgbuild_cmd
        backtick(pkgbuild_cmd)

        productbuild = "/usr/bin/productbuild"
        productbuild_cmd = ' '.join([productbuild,
                                     "--resources %s" % resources_dir,
                                     "--distribution %s" % distribution_xml,
                                     # "--sign '%s'" % identity,
                                     "--package-path %s" % working_dir,
                                     "--quiet",
                                     temp])
        print productbuild_cmd
        backtick(productbuild_cmd)

        productsign = "/usr/bin/productsign"
        productsign_cmd = ' '.join([productsign,
                                    "-s '%s'" % self.identity,
                                    "'%s'" % temp,
                                    "'%s'" % output])
        print productsign_cmd
        backtick(productsign_cmd)
        os.remove(temp)

        os.chdir(old_cwd)
        self.verify_codesign (output)
        return output

    def verify_codesign(self, pkg):
        oldcwd = os.getcwd()
        try:
            name = os.path.basename(pkg)
            pkgdir = os.path.dirname(pkg)
            os.chdir(pkgdir)
            spctl = "/usr/sbin/spctl"
            spctl_cmd = ' '.join(
                [spctl, "-vvv", "--assess", "--type install", name, "2>&1"])
            output = backtick(spctl_cmd)

            if "accepted" in " ".join(output):
                warn ("%s IS SIGNED" % pkg)
            else:
                error ("%s IS NOT SIGNED:" % pkg)
        finally:
            os.chdir(oldcwd)

    # THIS IS THE MAIN METHOD FOR MAKING A PACKAGE
    def package(self):
        MonoReleaseProfile.package (self)

MonoXamarinPackageProfile().build()

