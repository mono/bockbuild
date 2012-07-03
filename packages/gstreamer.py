class GstreamerBasePackage (GstreamerPackage):
        def __init__ (self):
                GstreamerPackage.__init__ (self,
                        project  = 'gstreamer',
                        name = 'gstreamer',
                        version = '0.10.36')

                self.configure = './configure --disable-gtk-doc --prefix="%{prefix}"'

                # Mark pluginloader changes to be reverted 
		self.sources.append ( 'http://cgit.freedesktop.org/gstreamer/gstreamer/patch/?id=f660536eb341767fbef0ccf1bf1139e2b4ce749c' )
		self.sources.append ( 'http://cgit.freedesktop.org/gstreamer/gstreamer/patch/?id=918a62abcf7ae44b0bc84d57742d2f759e0d8ed6' )
		self.sources.append ( 'http://cgit.freedesktop.org/gstreamer/gstreamer/patch/?id=159cf687a1b63f334ecec5e0b1ea4cd1bc8e7537' )  

        def prep (self):
                Package.prep (self)
                self.sh ('patch -p1 -R < "%{sources[1]}"')
                self.sh ('patch -p1 -R < "%{sources[2]}"')
                self.sh ('patch -p1 -R < "%{sources[3]}"')

GstreamerBasePackage ()
