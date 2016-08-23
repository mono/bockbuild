import os


class MonoLlvmPackage (GitHubPackage):

    def __init__(self):

        LLVM_CFLAGS='-I$TOP_DIR/include -D__STDC_CONSTANT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS -DNDEBUG -D__NO_CTYPE_INLINE -D_GNU_SO'
        LLVM_CXXFLAGS=LLVM_CFLAGS + '-std=c++11 -D__STDC_CONSTANT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS  -fvisibility-inlines-hidden'

        LLVM_CFLAGS='"' + LLVM_CFLAGS + '"'
        LLVM_CXXFLAGS='"' + LLVM_CXXFLAGS + '"'


        GitHubPackage.__init__(self, 'mono', 'llvm', '3.9',
                               git_branch='mono-2016-02-13-2acdc6d60c5199a3b8957d851b62691d71756d08',
                               configure="mkdir build ; cd build ; cmake ",
                               configure_flags=[
                                   '-DCMAKE_BUILD_TYPE=Release', '-DCMAKE_INSTALL_PREFIX="%{package_prefix}"',
                                   '-DCMAKE_C_FLAGS=', LLVM_CFLAGS, ' -DCMAKE_CXX_FLAGS=', LLVM_CXXFLAGS, 
                                   '../' # Path argument
                               ])

        self.ld_flags = []  # TODO: find out which flags are causing issues. reset ld_flags for the package
        self.cpp_flags = []

        # We want to use the variables set before this, so we need to group the commands with bash
        self.make = "bash -c 'cd build ; " + self.make + "'"

        self.skip_for_arch = False

    def install(self):
        if self.skip_for_arch:
            return

        unprotect_dir(self.stage_root)

        makeinstall_cmds = []
        makeinstall_cmds.append("cd build")
        makeinstall_cmds.append("make install DESTDIR=%{stage_root}")

        self.makeinstall = "bash -c '" + " ; ".join(makeinstall_cmds)  + "'"
        Package.install(self)

    def arch_build(self, arch):
        if arch == 'darwin-32':
            self.skip_for_arch = True
        # FIXME: Still applicable? No equivalent CMAKE flag
        # LLVM says that libstdc++4.6 is broken and we should use libstdc++4.7.
        # This switches it to the right libstdc++.
        # if Package.profile.name == 'darwin':
            # self.local_configure_flags.extend(['--enable-libcpp=yes'])
        pass

MonoLlvmPackage()
