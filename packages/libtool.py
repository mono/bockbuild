class LibtoolPackage (GnuPackage):

    def __init__(self):
        GnuPackage.__init__(
            self, 'libtool', '2.4.2', override_properties={'build_dependency': True})

    def install(self):
        Package.install(self)
        self.sh('rm -f "%{staged_prefix}/bin/glibtool"')
        self.sh(
            'ln -s "%{staged_prefix}/bin/libtool"  "%{staged_prefix}/bin/glibtool"')
        self.sh('rm -f "%{staged_prefix}/bin/glibtoolize"')
        self.sh(
            'ln -s "%{staged_prefix}/bin/libtoolize"  "%{staged_prefix}/bin/glibtoolize"')

LibtoolPackage()
