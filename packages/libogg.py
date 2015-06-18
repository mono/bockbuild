class LiboggPackage (XiphPackage):
        def __init__ (self):
                XiphPackage.__init__ (self,
                        project  = 'ogg',
                        name = 'libogg',
                        version = '1.3.0')

                self.configure = 'autoreconf -fi && ./configure --prefix="%{prefix}"'

		# reduce optimization from -O4 to -O3 to allow compilation on Xcode 4.2.1
                self.sources.append (Patch('patches/libogg-opt.patch', '-p1'))

        def prep (self):
                Package.prep (self)
                for patch in self.patches:
                        patch.run(self)

LiboggPackage ()
