import os

import sys, inspect

from mono_master import MonoMasterPackage

class MonoMasterEncryptedPackage (MonoMasterPackage):
    
    def __init__(self):
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

