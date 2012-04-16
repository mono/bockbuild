#!/bin/bash -x

if test x$1 = x; then
   echo usage is cleanup MONODIR
   exit 1
fi

MONODIR=$1

cd $MONODIR
rm -rf lib/gtk-2.0/2.10.0/engines/libcrux-engine.so
rm -rf lib/gtk-2.0/2.10.0/engines/libglide.so
rm -rf lib/gtk-2.0/2.10.0/engines/libhcengine.so
rm -rf lib/gtk-2.0/2.10.0/engines/libindustrial.so
rm -rf lib/gtk-2.0/2.10.0/engines/libmist.so
rm -rf lib/gtk-2.0/2.10.0/engines/libpixmap.so
rm -rf lib/gtk-2.0/2.10.0/engines/libredmond95.so
rm -rf lib/gtk-2.0/2.10.0/engines/libthinice.so
rm -rf gtk-2.0/modules/libferret.*
rm -rf gtk-2.0/modules/libgail.*
rm -rf share/gtk-2.0/demo/*
rm -rf share/man/man1/oldmono.1
rm -rf share/themes/Crux
rm -rf share/themes/Default
rm -rf share/themes/Emacs
rm -rf share/themes/Industrial
rm -rf share/themes/Mist
rm -rf share/themes/Raleigh
rm -rf share/themes/Redmond
rm -rf share/themes/ThinIce
rm -rf share/info
rm -rf share/icons/gnome
rm -rf share/icons/hicolor
rm -rf share/gettext/*.class
