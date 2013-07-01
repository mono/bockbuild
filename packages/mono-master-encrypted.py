import os


class MonoMasterEncryptedPackage(Package):

    def __init__(self):
	if os.getenv('MONO_VERSION') == None
		raise Exception ('You must export MONO_VERSION to use this build profile. e.g. export MONO_VERSION=3.1.0')

        Package.__init__(self, 'mono', os.getenv('MONO_VERSION'),
                         sources=[
                             'git://github.com/mono/mono.git',
                             'git@github.com:xamarin/mono-extensions.git'],
                         revision=os.getenv('MONO_BUILD_REVISION'),
                         configure_flags=[
                             '--enable-nls=no',
                             '--prefix=' + Package.profile.prefix,
                             '--with-ikvm=yes',
                             '--with-moonlight=no'
                         ])

        if Package.profile.name == 'darwin':
            self.configure_flags.extend([
                # fix build on lion, it uses 64-bit host even with -m32
                '--build=i386-apple-darwin11.2.0',
                '--enable-loadedllvm'
            ])

        self.sources.extend([
            # Fixes up pkg-config usage on the Mac
            'patches/mcs-pkgconfig.patch'
        ])

        self.configure = 'CFLAGS=-O2 ./autogen.sh'
        self.make = 'make'

    def apply_extensions(self):
        # Copied from Package#prep, makes sure we get the latest
        # extensions
        ext = self.sources[1]
        build_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
        dirname = os.path.join(build_root, "mono-extensions")
        if not os.path.exists(dirname):
            self.sh('%' + '{git} clone --local --shared "%s" "%s"' % (ext, dirname))
            self.cd(dirname)
            self.sh('%{git} clean -xfd')
            self.sh('%{git} pull')

        # Use quilt to apply the patch queue
        self.cd(build_root)
        mono = os.path.join(build_root, "mono")
        full_mono = os.path.join(build_root, self.name + "-" + self.version)
        full_mono_extensions = os.path.join(build_root, "mono-extensions")

        if not os.path.exists(mono):
            os.symlink(full_mono, mono)
        else:
            mono_link = os.path.join(os.path.dirname(mono), os.readlink(mono))
            if not (mono_link == full_mono):
                os.remove(mono)
                os.symlink(full_mono, mono)

        # ignore 'quilt pop' return code because the tree might be pristine
        prologue = "cd %s; export QUILT_PATCHES=mono-extensions" % build_root
        self.sh("%s; /usr/local/bin/quilt upgrade || true" % prologue)
        self.sh("%s; /usr/local/bin/quilt pop -af || true" % prologue)
        self.sh("%s; /usr/local/bin/quilt push -a" % prologue)

        # Print mono-extensions commit hash and the patches applied
        commit_hash = backtick("git --git-dir %s/.git rev-parse HEAD" % full_mono_extensions)[0]
        patches_applied = backtick("cd %s; /usr/local/bin/quilt applied" % build_root)
        self.sh("echo '@MonkeyWrench: SetSummary: <p>Using mono-extensions %s</p><p>Applied patches:<br>%s</p>'" % (commit_hash[0:8], "<br>".join(patches_applied)))

    def prep(self):
        Package.prep(self)
        self.apply_extensions()
        self.cd('%{source_dir_name}')
        if Package.profile.name == 'darwin':
            for p in range(2, len(self.sources)):
                self.sh('patch -p1 < "%{sources[' + str(p) + ']}"')

MonoMasterEncryptedPackage()
