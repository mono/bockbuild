MD_BUILD_EXE="../../../monodevelop/main/build/bin/MonoDevelop.exe"
MD_APP_EXE="../../../md-addins/Xamarin Studio.app/Contents/MacOS/lib/monodevelop/bin/XamarinStudio.exe"
MONO_OPTIONS=--gc=sgen --debug
MD_OPTIONS=--no-redirect


all:
	./monodevelop-mac-dev.py -b

run:
	mono $(MONO_OPTIONS) $(MD_BUILD_EXE) $(MD_OPTIONS)

run-app:
	mono $(MONO_OPTIONS) $(MD_APP_EXE) $(MD_OPTIONS)

