class MonobjcPackage (Package):

    def __init__(self):
        Package.__init__(self, 'Monobjc', '2.0.479.0', sources=[
            'http://downloads.monobjc.net/%{name}-%{version}.tar.gz',
            'patches/monobjc/Makefile',
            'patches/monobjc/nant-disable-native-enable-debug.patch',
            'patches/monobjc/remove-executable-path-dllimport.patch',
            'patches/monobjc/PkgConfigGenerator.cs'
        ])

        self.dylib_compatibility_version = '2.0.0'
        self.dylib_current_version = '2.4.79'

    def prep(self):
        # Create and extract into top-level directory
        # since Monobjc is archived incorrectly
        self.sh('mkdir "%{source_dir_name}"')
        self.cd('%{source_dir_name}')
        self.sh('tar xf "%{sources[0]}"')

        # Remove the binaries that come with the release
        self.sh('rm -rf -- dist')

        # Install a proper Makefile that builds properly
        self.sh('cp "%{sources[1]}" src/native/Monobjc/src')

        # Disable native and 1.0 profile builds in nant,
        # and enable debugging (produce .mdb files)
        self.sh('patch -p1 < "%{sources[2]}"')

        # Remove the @executable_path/ prefix from the
        # DllImport attributes for libmonobjc.2.dylib
        self.sh('patch -p1 < "%{sources[3]}"')

    def build(self):
        # Build the managed libraries
        self.sh('nant build-libraries')

        # Build the native library
        self.pushd('src/native/Monobjc/src')
        self.sh(
            'make COMPATIBILITY_VERSION=%{dylib_compatibility_version} CURRENT_VERSION=%{dylib_current_version}')
        self.popd()

        # Build the pkg-config generator
        self.sh('gmcs -out:pc-gen.exe "%{sources[4]}"')

    def install(self):
        # Install assemblies into the GAC, generate a pkg-config file
        self.sh('mkdir -p "%{prefix}/share/pkgconfig"')
        for path in glob.glob('dist/2.0/*.dll'):
            basename = os.path.basename(path)
            pkgconfig = os.path.splitext(basename)[0] + '.pc'
            self.sh('gacutil -i -package Monobjc -root "%{prefix}/lib" "' +
                    path + '"')
            self.sh('mono pc-gen.exe "%{prefix}/lib/mono/Monobjc/' +
                    basename + '" > "%{prefix}/share/pkgconfig/' + pkgconfig + '"')

        # Install native library into the standard lib dir
        self.sh(
            'cp "src/native/Monobjc/src/libmonobjc.2.dylib" "%{prefix}/lib"')

MonobjcPackage()
