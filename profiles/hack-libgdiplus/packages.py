import os


class HackGDIPlusPackages:
    def __init__(self):

        # Toolchain
        self.packages.extend([
            'xz.py',
            'tar.py',
            'autoconf.py',
            'automake.py',
            'libtool.py',
            'gettext.py',
            'pkg-config.py',
        ])

        # # Base Libraries
        self.packages.extend([
            'libpng.py',
            'libjpeg.py',
            'libtiff.py',
            'libgif.py',
            'libxml2.py',
            'freetype.py',
            'fontconfig.py',
            'pixman.py',
            'cairo.py',
            'libffi.py',
            'glib.py'
        ])

        # Mono
        self.packages.extend(['libgdiplus.py'])

        self.packages = [os.path.join('..', '..', 'packages', p) for p in self.packages]
