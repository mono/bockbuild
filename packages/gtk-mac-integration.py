class Gtkmacintegration (GnomeXzPackage):

    def __init__(self):
        GnomeXzPackage.__init__(self, 'gtk-mac-integration',
                                version_major='1.0',
                                version_minor='1',
                                sources=[
                                    'ftp://ftp.gnome.org/pub/gnome/sources/gtk-mac-integration/1.0/%{name}-%{version}.tar.xz'],
                                configure_flags=[
                                    '--prefix="%{prefix}"'
                                ])

        self.sources.extend([
            # fix Alt/Mod1 key behaviour on OS X - required
            # for key accelerators using the alt/option key on OSX
            'http://git.gnome.org/browse/gtk-mac-integration/patch/?id=19cf4ee74821aa5d6d70d0a069178fa5a684ff7f'
        ])

    def prep(self):
        Package.prep(self)
        if Package.profile.name == 'darwin':
            for p in range(1, len(self.local_sources)):
                self.sh('patch -p1 < "%{local_sources[' + str(p) + ']}"')

Gtkmacintegration()
