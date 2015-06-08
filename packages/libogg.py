class LiboggPackage (XiphPackage):

    def __init__(self):
        XiphPackage.__init__(self,
                             project='ogg',
                             name='libogg',
                             version='1.3.0')

        self.configure = 'autoreconf -fi && ./configure --prefix="%{prefix}"'

        # reduce optimization from -O4 to -O3 to allow compilation on Xcode
        # 4.2.1
        self.sources.append('patches/libogg-opt.patch')

    def prep(self):
        Package.prep(self)
        self.sh('patch -p1 < "%{local_sources[1]}"')

LiboggPackage()
