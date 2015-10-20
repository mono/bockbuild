from mono_master import MonoMasterPackage

class MonoMasterEncryptedPackage (MonoMasterPackage):
    
    def __init__(self):
        MonoMasterPackage.__init__ (self)

        self.configure_flags.extend(['--enable-extension-module=crypto --enable-native-types'])

MonoMasterEncryptedPackage()