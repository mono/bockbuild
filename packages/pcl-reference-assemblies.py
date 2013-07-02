import glob
import os


class PCLReferenceAssembliesPackage(Package):
    def __init__(self):
        Package.__init__(self,
                         name='PortableReferenceAssemblies',
                         version='2013-06-27',
                         sources=['http://storage.bos.xamarin.com/bot-provisioning/PortableReferenceAssemblies2013-06-27.zip'])

    def prep(self):
        pass

    def build(self):
        pass

    # A bunch of shell script written inside python literals ;(
    def install(self):
        dest = "/Library/Frameworks/Mono.framework/External/xbuild-frameworks/.NETPortable/"
        if not os.path.exists(dest):
            os.mkdir(dest)
        self.sh("unzip -o -q %s -d %s" % (self.sources[0], dest))

        name = expand_macros("%{name}%{version}", self)
        pcldir = os.path.join(dest, name)
        self.sh("rsync -abv --remove-source-files -q %s/* %s" % (pcldir, dest))
        self.sh("rm -rf " + pcldir)

        for f in glob.glob("*/Profile/*/SupportedFrameworks"):
            self.write_xml(os.path.join(dest, f))

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
