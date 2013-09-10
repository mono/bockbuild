import glob
import os
import shutil


class PCLReferenceAssembliesPackage(Package):
    def __init__(self):
        Package.__init__(self,
                         name='PortableReferenceAssemblies',
                         version='2013-09-10',
                         sources=['http://last-hope.baulig.net/misc/mono-pcl-profiles.tgz'])
        self.source_dir_name = "mono-pcl-profiles"

    def prep(self):
        self.extract_archive(self.sources[0],
                             validate_only=False,
                             overwrite=True)

    def build(self):
        pass

    # A bunch of shell script written inside python literals ;(
    def install(self):
        dest = os.path.join(self.prefix, "lib", "mono", "xbuild-frameworks", ".NETPortable")
        if not os.path.exists(dest):
            os.makedirs(dest)

        shutil.rmtree(dest, ignore_errors=True)

        pcldir = os.path.join(self.package_build_dir(), self.source_dir_name)
        self.sh("rsync -abv -q %s/* %s" % (pcldir, dest))

        # Remove v4.6 until we support it
        shutil.rmtree(os.path.join(dest, "v4.6"))

PCLReferenceAssembliesPackage()
