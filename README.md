Note: This is the actively maintained version of Bockbuild, used to put together the Mono Mac framework package for OS X. The legacy versions (used for Banshee and older Mono versions) are available here: https://github.com/mono/bockbuild/tree/legacy

The Mono Mac distribution
-------------------------

To build the distribution with the very latest Mono, download :

    $ git clone git@github.com:mono/bockbuild bockbuild
    $ cd bockbuild/profiles/mono-mac
    $ ./mono-mac.py --build --arch darwin-32

`--arch` can also be `darwin-64` or `darwin-universal` (32/64 lipoed build).

To build the distribution with a Mono from a branch:

    $ MONO_BRANCH=mono-4.4.0-branch ./mono-mac.py --build --arch darwin-32
    
To build the distribution with your local copy of Mono:

    $ MONO_REPOSITORY=/your/mono ./mono-mac.py --build --arch darwin-32

To get a shell that uses your custom-built distribution (e.g. to build & run Monodevelop against it):

    $ MONO_BRANCH=mono-4.4.0-branch ./mono-mac.py --shell
    
Finally, to create a package of the distribution:

    $ MONO_BRANCH=mono-4.4.0-branch ./mono-mac.py --build --package

Xamarin Releases
----------------

Release packages are built with the following:

    $ cd bockbuild/profiles/mono-mac-xamarin
    $ ./mono-mac-xamarin.py --build --package --release --arch darwin-32


