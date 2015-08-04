import os


class MonoMasterEncryptedPackage(Package):

    def __init__(self):
        if os.getenv('MONO_BRANCH') is None:
            raise Exception('You must export MONO_BRANCH to use this build profile. e.g. export MONO_BRANCH=master')

        if os.getenv('MONO_BUILD_REVISION') is None:
            warn ('MONO_BUILD_REVISION not set, using HEAD of %s' % os.getenv('MONO_BRANCH'))

        Package.__init__(self, 'mono', os.getenv('MONO_VERSION'),
                         sources=[
                             'git://github.com/mono/mono.git',
                             'git@github.com:xamarin/mono-extensions.git'],
                         git_branch = os.getenv ('MONO_BRANCH') or None,
                         revision=os.getenv('MONO_BUILD_REVISION'),
                         configure_flags=[
                             '--enable-nls=no',
                             '--prefix=' + Package.profile.prefix,
                             '--with-ikvm=yes',
                             '--with-moonlight=no'
                         ])
        #This package would like to be lipoed.
        self.needs_lipo = True

        if Package.profile.name == 'darwin':
            self.configure_flags.extend([
                '--with-libgdiplus=%s/lib/libgdiplus.dylib' % Package.profile.prefix,
                '--enable-loadedllvm',
                'CXXFLAGS=-stdlib=libc++'
                ])

        self.configure_flags.extend(['--enable-extension-module=crypto --enable-native-types'])

        self.sources.extend([
            # Fixes up pkg-config usage on the Mac
            'patches/mcs-pkgconfig.patch'
        ])

        self.gcc_flags.extend (['-O2'])

        self.configure = './autogen.sh --prefix="%{package_prefix}"'

    def checkout_mono_extensions(self):
        ext = self.sources[1]
        dirname = os.path.join(self.profile.build_root, "mono-extensions")

        if not os.path.exists(dirname):
            self.sh('%' + '{git} clone --local --shared "%s" "%s"' % (ext, dirname))
        try:
            self.pushd(dirname)
            self.sh('%{git} clean -xfd')
            self.sh('%{git} fetch --all --prune')
            if "pr/" not in os.getenv('MONO_BRANCH'):
                self.sh('%' + '{git} checkout origin/%s' % os.getenv('MONO_BRANCH'))
            else:
                self.sh('%{git} checkout origin/master')
        except Exception as e:
            self.popd (failure = True)
            self.rm_if_exists (dirname)
        finally:
            self.popd ()

    def prep(self):
        Package.prep(self)
        source_dir = os.getcwd()      
        dest_dir = os.path.join(self.profile.build_root, "mono")

        if os.path.exists (dest_dir):
            self.rm (dest_dir)

        self.sh("ln -s %s %s" % (source_dir, dest_dir))
        retry (self.checkout_mono_extensions)

        self.cd(source_dir)

        if Package.profile.name == 'darwin':
            for p in range(2, len(self.sources)):
                self.sh('patch -p1 < "%{local_sources[' + str(p) + ']}"')

    def arch_build (self, arch):    
        if arch == 'darwin-64': #64-bit build pass
            self.local_gcc_flags = ['-m64']
            self.local_configure_flags = ['--build=x86_64-apple-darwin11.2.0']
        
        if arch == 'darwin-32': #32-bit build pass
            self.local_gcc_flags =['-m32']
            self.local_configure_flags = ['--build=i386-apple-darwin11.2.0']

    def build(self):
        Package.build (self)
        self.sh ('%{make} -C mono/metadata/ pecrypt')

    def install(self):
        Package.install (self)
        self.extra_stage_files = ['etc/mono/config']

        registry_dir = os.path.join(self.staged_prefix, "etc", "mono", "registry", "LocalMachine")
        if not os.path.exists(registry_dir):
            os.makedirs(registry_dir)

MonoMasterEncryptedPackage()
