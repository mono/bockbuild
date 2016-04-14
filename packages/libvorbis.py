class LibvorbisPackage (XiphPackage):

    def __init__(self):
        XiphPackage.__init__(self,
                             project='vorbis',
                             name='libvorbis',
                             version='1.3.2')
        self.configure = './configure --prefix="%{prefix}"'

        # reduce optimization from -O4 to -O3 to allow compilation on Xcode
        # 4.2.1
        self.sources.append('patches/libvorbis-opt.patch')

    def prep(self):
        Package.prep(self)
        self.sh('patch -p1 < "%{local_sources[1]}"')

LibvorbisPackage()
