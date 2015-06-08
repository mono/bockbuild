class TarPackage (GnuPackage):

    def __init__(self):
        GnuPackage.__init__(self, 'tar', '1.26',
                            configure_flags=[
                                '--enable-nls=no'
                            ],
                            override_properties={'build_dependency': True}
                            )

TarPackage()
