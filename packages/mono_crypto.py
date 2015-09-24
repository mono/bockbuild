from mono_master import MonoMasterPackage
from bockbuild.util.util import *

class MonoMasterEncryptedPackage (MonoMasterPackage):
    
    def __init__(self):
        info ('Mono includes crypto extensions')
        MonoMasterPackage.__init__ (self)

        self.configure_flags.extend(['--enable-extension-module=crypto --enable-native-types'])

    def prep(self):
        MonoMasterPackage.prep(self)
        retry (self.checkout_mono_extensions)

    def checkout_mono_extensions(self):
        ext = 'git@github.com:xamarin/mono-extensions.git'
        dirname = os.path.join(self.profile.build_root, "mono-extensions")

        if not os.path.exists(dirname):
            self.sh('%' + '{git} clone --local --shared "%s" "%s"' % (ext, dirname))

        self.pushd(dirname)
        try:
            self.sh('%{git} clean -xffd')
            self.sh('%{git} fetch --all --prune')
            if "pr/" not in self.git_branch:
                self.sh('%' + '{git} checkout origin/%s' % self.git_branch)
            else:
                self.sh('%{git} checkout origin/master')
        except Exception as e:
            self.rm_if_exists (dirname)
            raise
        finally:
            self.popd ()

MonoMasterEncryptedPackage()