
The Mono Mac distribution
-------------------------

To build the distribution with the very latest Mono:

    $ git clone git@github.com:mono/bockbuild bockbuild
    $ cd bockbuild/profiles/mono-mac-release
    $ MONO_VERSION=4.9.9 ./mono-mac-release.py --build --arch darwin-32
`MONO_VERSION` can be any number formatted as X.X.X.

`--arch` can also be `darwin-64` or `darwin-universal` (32/64 lipoed build).

To build the distribution with a Mono from a branch:

    $ MONO_VERSION=4.9.9 MONO_BRANCH=mono-4.0.0-branch ./mono-mac-release.py --build --arch darwin-32
    
To build the distribution with your local copy of Mono:

    $ MONO_REPOSITORY=/your/mono ./mono-mac-release.py --build --arch darwin-32

To get a shell that uses your custom-built distribution (e.g. to build & run Monodevelop against it):

    $ MONO_VERSION=4.9.9 MONO_BRANCH=mono-4.0.0-branch ./mono-mac-release.py --shell
    
Finally, to create a package of the distribution:

    $ MONO_VERSION=4.9.9 MONO_BRANCH=mono-4.0.0-branch ./mono-mac-release.py --build --package


Bockbuild
---------

bockbuild is a light-weight build system that can both build and shape bundles
for GTK/Mono applications on OS X. Building is easily supported for both Linux
and Windows as well.

A build profile can be defined to build a complete jail of dependencies to
allow for locally running applications from source without affecting the
system libraries or other environment.

It was initially developed to build all of Banshee's dependencies and shape
them into a .app bundle.

solitary is the component that walks top-level components of an application
to collect all of their dependencies. It is technically a standalone component
that works against both native and managed code, resulting in a relocatable
application structure. Currently it only works for native code on OS X/darwin.
