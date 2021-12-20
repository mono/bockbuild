class MurrinePackage (GnomeXzPackage):

    def __init__(self):
        GnomePackage.__init__(self,
                              'murrine',
                              version_major='0.98',
                              version_minor='2')

        # FIXME: this may need porting
        # self.sources.append ('patches/murrine-osx.patch')
	self.sources.append ('patches/murrine-prototypes.patch')

    def prep(self):
        GnomeXzPackage.prep(self)
        if Package.profile.name == 'darwin':
            for p in range(1, len(self.local_sources)):
                self.sh('patch -p1 < "%{local_sources[' + str(p) + ']}"')

        Package.prep(self)

MurrinePackage()
