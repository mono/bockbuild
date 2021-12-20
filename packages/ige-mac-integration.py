class IgePackage(SourceForgePackage):
    def __init__(self):
        SourceForgePackage.__init__(self, 'gtk-osx', 'ige-mac-integration', '0.9.4', ['--without-compile-warnings'],
                   override_properties={'configure': './configure --prefix="%{staged_prefix}"',
                                        'makeinstall': 'make install'})
        self.sources.extend(["patches/ige-arm64.patch"])

    def prep(self):
        SourceForgePackage.prep(self)
        if Package.profile.name == 'darwin':
            for p in range(1, len(self.local_sources)):
                self.sh('patch -p1 < "%{local_sources[' + str(p) + ']}"')

IgePackage()
