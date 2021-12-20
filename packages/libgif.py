class LibgifPackage (SourceForgePackage):

    def __init__(self):
        SourceForgePackage.__init__(self, 'giflib', 'giflib', '4.1.6')
        self.sources.extend([
            'patches/libgif/libgif.patch'
        ])

    def build(self):
        if Package.profile.name == 'darwin':
            Package.configure(self)
            for p in range(1, len(self.local_sources)):
                self.sh('patch -u lib/gif_hash.c -i %{local_sources[' + str(p) + ']}')
            Package.make(self)
        else:
            Package.build(self)

LibgifPackage()