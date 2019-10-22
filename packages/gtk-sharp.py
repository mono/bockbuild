class GtkSharp212ReleasePackage (Package):

    def __init__(self):
        Package.__init__(self, 'gtk-sharp',
                         sources=['git://github.com/mono/gtk-sharp.git'],
                         git_branch='gtk-sharp-2-12-branch',
                         revision='a663d4ee3e8d97376bc4e561d9ed3fd7f31a6ace',
                         override_properties={
                             'configure': './bootstrap-2.12 --prefix=%{package_prefix}',
                         }
                         )

GtkSharp212ReleasePackage()
