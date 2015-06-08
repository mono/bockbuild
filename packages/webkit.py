class WebkitPackage (Package):

    def __init__(self):
        Package.__init__(self, 'webkit', '1.8.1',
                         sources=[
                             'http://webkitgtk.org/releases/%{name}-%{version}.tar.xz'
                         ],
                         configure_flags=[
                             '--disable-video',
                             '--disable-geolocation',
                             '--disable-xslt',
                         ]
                         )

        if Package.profile.name == 'darwin':
            self.configure_flags.extend([
                '--with-target=quartz',
                '--with-gtk=2.0',
                '--disable-gtk-doc'
            ])

            self.sources.extend([
                # disable xrender when building with quartz, see
                # https://trac.macports.org/attachment/ticket/34086/xrender-check.patch
                'https://trac.macports.org/raw-attachment/ticket/34086/xrender-check.patch'
            ])

    def prep(self):
        Package.prep(self)
        if Package.profile.name == 'darwin':
            for p in range(1, len(self.sources)):
                self.sh('patch -p0 < "%{local_sources[' + str(p) + ']}"')

WebkitPackage()
