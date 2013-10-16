import glob
import os
import shutil


class PCLReferenceAssembliesPackage(Package):
    def __init__(self):
        Package.__init__(self,
                         name='mono-pcl-profiles',
                         version='2013-10-15',
                         sources=['http://storage.bos.xamarin.com/mono-pcl/e3/e3cf5cbc5b0607e29e0d68c67d36c8c9de91e0a1/mono-pcl-profiles.tar.gz'])
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

PCLReferenceAssembliesPackage()
