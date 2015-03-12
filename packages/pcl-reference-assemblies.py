import glob
import os
import shutil


class PCLReferenceAssembliesPackage(Package):
    def __init__(self):
        Package.__init__(self,
                         name='PortableReferenceAssemblies',
                         version='2014-04-14',
                         sources=['http://storage.bos.xamarin.com/bot-provisioning/PortableReferenceAssemblies-2014-04-14.zip'])

    def prep(self):
        self.extract_archive(self.sources[0],
                             validate_only=False,
                             overwrite=True)

    def build(self):
        pass

    # A bunch of shell script written inside python literals ;(
    def install(self):
        dest = os.path.join(self.staged_prefix, "lib", "mono", "xbuild-frameworks", ".NETPortable")
        if not os.path.exists(dest):
            os.makedirs(dest)

        shutil.rmtree(dest, ignore_errors=True)

        # Omit v4.6 until we support it
        pcldir = os.path.join(self.Package.profile.build_root, self.source_dir_name)

        self.sh("rsync -abv -q --exclude '%s' %s/* %s" % ("v4.6", pcldir, dest))

        for f in glob.glob("%s/*/Profile/*/SupportedFrameworks" % dest):
            self.write_xml(f)

    def write_xml(self, directory):
        print "Writing iOS/Android/Mac listings for " + directory
        data = {
            os.path.join(directory, "MonoTouch.xml"):
            """<Framework Identifier="MonoTouch" MinimumVersion="1.0" Profile="*" DisplayName="Xamarin.iOS Classic"/>""",
            os.path.join(directory, "Xamarin.iOS.xml"):
            """<Framework Identifier="Xamarin.iOS" MinimumVersion="1.0" Profile="*" DisplayName="Xamarin.iOS Unified"/>""",
            os.path.join(directory, "Xamarin.Android.xml"):
            """<Framework Identifier="MonoAndroid" MinimumVersion="1.0" Profile="*" DisplayName="Xamarin.Android"/>""",
            os.path.join(directory, "Xamarin.Mac.xml"):
            """<Framework Identifier="Xamarin.Mac" MinimumVersion="2.0" Profile="*" DisplayName="Xamarin.Mac Unified"/>""",
        }
        for filename, content in data.iteritems():
            f = open(filename, "w")
            f.write(content + "\n")
            f.close()


PCLReferenceAssembliesPackage()
