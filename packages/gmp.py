class GmpPackage (Package):

    def __init__(self):
        Package.__init__(self, 'gmp', '5.0.4', sources=[
            'ftp://ftp.gmplib.org/pub/%{name}-%{version}/%{name}-%{version}.tar.bz2'
        ],
            configure_flags=['--enable-cxx --disable-dependency-tracking'])

        if Package.profile.name == 'darwin':
            self.configure_flags.extend(['ABI=32'])

GmpPackage()
