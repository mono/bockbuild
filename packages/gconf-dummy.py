class Gconf2DummyPackage (Package):

    def __init__(self):
        Package.__init__(self, 'gconf2-dummy', '2')

    def install(self):
        self.sh('echo "AC_DEFUN([AM_GCONF_SOURCE_2],[])" '
                '> %{prefix}/share/aclocal/gconf-2.m4')

Gconf2DummyPackage()
