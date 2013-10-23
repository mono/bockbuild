import glob
import os
import shutil


class PCLReferenceAssembliesPackage(Package):
    def __init__(self):
        Package.__init__(self,
                         name='mono-pcl-profiles',
                         version='2013-10-23',
                         sources=['http://storage.bos.xamarin.com/mono-pcl/58/5825e0404974d87799504a0df75ea4dca91f9bfe/mono-pcl-profiles.tar.gz'])
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

        pcldir = os.path.join(self.package_build_dir(), self.source_dir_name, ".NETPortable")
        self.sh("rsync -abv -q %s/* %s" % (pcldir, dest))

PCLReferenceAssembliesPackage()
