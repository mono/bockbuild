class LibtoolPackage (GnuPackage):
        def __init__ (self):
                GnuPackage.__init__ (self, 'libtool', '2.4.2')

        def install (self):
		Package.install (self)
		self.sh ('rm -f "%{prefix}/bin/glibtool"')
                self.sh ('ln -s "%{prefix}/bin/libtool"  "%{prefix}/bin/glibtool"')
                self.sh ('rm -f "%{prefix}/bin/glibtoolize"')
                self.sh ('ln -s "%{prefix}/bin/libtoolize"  "%{prefix}/bin/glibtoolize"')


LibtoolPackage ()
