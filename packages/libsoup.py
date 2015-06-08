class LibsoupPackage (GnomePackage):

    def __init__(self):
        GnomePackage.__init__(self, 'libsoup', '2.33', '90')
        self.configure_flags = [
            '--disable-gtk-doc',
            '--without-gnome'
        ]

LibsoupPackage()
