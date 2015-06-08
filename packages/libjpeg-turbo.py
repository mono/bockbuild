class LibJpegTurboPackage (SourceForgePackage):

    def __init__(self):
        SourceForgePackage.__init__(self, '%{name}', 'libjpeg-turbo', '1.3.0')

    def arch_build(self, arch):
        if arch == 'darwin-universal':
            self.local_configure_flags = [
                '--host x86_64-apple-darwin NASM=%{prefix}/bin/nasm']
        elif arch == 'darwin-32':
            self.local_configure_flags = [
                '--host i686-apple-darwin CFLAGS="-O3 -m32" LDFLAGS=-m32']
        elif arch == 'darwin-64':
            self.local_configure_flags = [
                '--host x86_64-apple-darwin NASM=%{prefix}/bin/nasm']

        Package.arch_build(self, arch, defaults=False)

LibJpegTurboPackage()
