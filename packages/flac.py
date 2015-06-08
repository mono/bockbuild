class FlacPackage (XiphPackage):

    def __init__(self):
        XiphPackage.__init__(self, 'flac', 'flac', '1.2.1',
                             configure_flags=[
                                 '--disable-cpplibs'
                             ]
                             )

        if Package.profile.name == 'darwin':
            self.configure_flags.append('--disable-asm-optimizations')

FlacPackage()
