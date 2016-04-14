class GtkQuartzEnginePackage (Package):

    def __init__(self):
        Package.__init__(self, 'gtk-quartz-engine',
                         sources=[
                             'git://github.com/mono/gtk-quartz-engine.git'],
                         override_properties={
                             'configure': './autogen.sh --prefix=%{package_prefix}',
                             'needs_lipo': True
                         },
                         revision='355d5f123281e88e2ec5bc2e5093cee8b13923fb')

GtkQuartzEnginePackage()
