class LibFfiPackage (Package):

    def __init__(self):
        Package.__init__(self, 'libffi', '3.3', configure_flags=["--build=aarch64-apple-darwin20.0.0"],
	    sources=[
            'ftp://sourceware.org/pub/%{name}/%{name}-%{version}.tar.gz'])

LibFfiPackage()
