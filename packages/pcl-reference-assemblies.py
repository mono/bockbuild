import glob
import os
import shutil


class PCLReferenceAssembliesPackage(Package):
    def __init__(self):
        Package.__init__(self,
                         name='PortableReferenceAssemblies',
                         version='2013-06-27',
                         sources=['http://storage.bos.xamarin.com/bot-provisioning/PortableReferenceAssemblies2013-06-27.zip'])
        self.source_dir_name = "PortableReferenceAssemblies2013-06-27"

    def prep(self):
        self.extract_archive(self.sources[0],
                             validate_only=True,
                             overwrite=True)

    def build(self):
        pass

    # A bunch of shell script written inside python literals ;(
    def install(self):
        dest = "/Library/Frameworks/Mono.framework/External/xbuild-frameworks/.NETPortable/"
        if not os.path.exists(dest):
            os.mkdir(dest)

        name = expand_macros("%{name}%{version}", self)
        pcldir = os.path.join(dest, name)
        shutil.rmtree(dest, ignore_errors=True)
        self.sh("rsync -abv -q %s/* %s" % (name, dest))

        for f in glob.glob("%s/*/Profile/*/SupportedFrameworks" % dest):
            self.write_xml(f)

    def write_xml(self, directory):
        print "Writing iOS/Android listings for " + directory
        data = {
            os.path.join(directory, "Xamarin.iOS.xml"):
            """<Framework Identifier="MonoTouch" MinimumVersion="1.0" Profile="*" DisplayName="Xamarin.iOS"/>""",
            os.path.join(directory, "Xamarin.Android.xml"):
            """<Framework Identifier="MonoAndroid" MinimumVersion="1.0" Profile="*" DisplayName="Xamarin.Android"/>"""
        }
        for filename, content in data.iteritems():
            f = open(filename, "w")
            f.write(content + "\n")
            f.close()

PCLReferenceAssembliesPackage()
