Mono Package with crypto extensions
-----------------------------------
For a signed release package (only for hosts with the Xamarin signing certificate):

    $ git clone git@github.com:xamarin/bockbuild xamarin_bockbuild
    $ cd xamarin_bockbuild/profiles/mono-mac-xamarin
    $ ./mono-mac-xamarin.py --build --package --release --arch darwin-32

For an unsigned package (e.g. for testing locally), remove the `--release` option:

    $ ./mono-mac-xamarin.py --build --package --arch darwin-32

For more usage instructions, see https://github.com/mono/bockbuild/blob/master/README.md
