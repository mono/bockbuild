#!/bin/bash -x

if test x$1 = x; then
   echo usage is cleanup MONODIR
   exit 1
fi

MONODIR=$1

cd $MONODIR
find . -name '*.la' -delete
find . -name '*.a' -delete
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

rm -rf bin/cilc
rm -rf bin/gapi2-codegen
rm -rf bin/gapi2-fixup
rm -rf bin/gapi2-parser
rm -rf bin/gdk-pixbuf-csource
rm -rf bin/glib-genmarshal
rm -rf bin/glib-gettextize
rm -rf bin/glib-mkenums
rm -rf bin/gobject-query
rm -rf bin/gtester
rm -rf bin/gtester-report
rm -rf bin/gtk-builder-convert
rm -rf bin/gtk-demo
rm -rf bin/gtk-query-immodules-2.0
rm -rf bin/libglade-convert
rm -rf bin/mjs
# Needed by MD
#rm -rf bin/msgfmt
#rm -rf bin/msgmerge

rm -rf lib/gettext/*

rm -rf lib/gtk-2.0/include

rm -rf lib/gtk-sharp-2.0/gapi-fixup.exe
rm -rf lib/gtk-sharp-2.0/gapi-parser.exe
rm -rf lib/gtk-sharp-2.0/gapi2xml.pl
rm -rf lib/gtk-sharp-2.0/gapi_codegen.exe
rm -rf lib/gtk-sharp-2.0/gapi_pp.pl


rm -rf lib/pkgconfig/atk.pc
rm -rf lib/pkgconfig/cairo*
rm -rf lib/pkgconfig/gail.pc
rm -rf lib/pkgconfig/gapi-2.0.pc
rm -rf lib/pkgconfig/gdk-2.0.pc
rm -rf lib/pkgconfig/gdk-pixbuf-2.0.pc
rm -rf lib/pkgconfig/gdk-quartz-2.0.pc
rm -rf lib/pkgconfig/gio-2.0.pc
rm -rf lib/pkgconfig/gio-unix-2.0.pc
rm -rf lib/pkgconfig/glib-2.0.pc
rm -rf lib/pkgconfig/gmodule-2.0.pc
rm -rf lib/pkgconfig/gmodule-export-2.0.pc
rm -rf lib/pkgconfig/gmodule-no-export-2.0.pc
rm -rf lib/pkgconfig/gobject-2.0.pc
rm -rf lib/pkgconfig/gthread-2.0.pc
rm -rf lib/pkgconfig/gtk+-2.0.pc
rm -rf lib/pkgconfig/gtk+-quartz-2.0.pc
rm -rf lib/pkgconfig/gtk+-unix-print-2.0.pc
rm -rf lib/pkgconfig/gtk-engines-2.pc
rm -rf lib/pkgconfig/ige-mac-integration.pc
rm -rf lib/pkgconfig/libgdiplus.pc
rm -rf lib/pkgconfig/libglade-2.0.pc
rm -rf lib/pkgconfig/libpng.pc
rm -rf lib/pkgconfig/libpng12.pc
rm -rf lib/pkgconfig/pango.pc
rm -rf lib/pkgconfig/pangocairo.pc
rm -rf lib/pkgconfig/pixman-1.pc
rm -rf lib/pkgconfig/sqlite3.pc

rm -rf include

rm -rf share/aclocal/codeset.m4
rm -rf share/aclocal/gettext.m4
rm -rf share/aclocal/glib-2.0.m4
rm -rf share/aclocal/glib-gettext.m4
rm -rf share/aclocal/glibc2.m4
rm -rf share/aclocal/glibc21.m4
rm -rf share/aclocal/gtk-2.0.m4
rm -rf share/aclocal/iconv.m4
rm -rf share/aclocal/intdiv0.m4
rm -rf share/aclocal/intl.m4
rm -rf share/aclocal/intldir.m4
rm -rf share/aclocal/intlmacosx.m4
rm -rf share/aclocal/intmax.m4
rm -rf share/aclocal/inttypes-pri.m4
rm -rf share/aclocal/inttypes_h.m4
rm -rf share/aclocal/lcmessage.m4
rm -rf share/aclocal/lib-ld.m4
rm -rf share/aclocal/lib-link.m4
rm -rf share/aclocal/lib-prefix.m4
rm -rf share/aclocal/lock.m4
rm -rf share/aclocal/longlong.m4
rm -rf share/aclocal/nls.m4
# Needed by MD
#rm -rf share/aclocal/pkg.m4
rm -rf share/aclocal/po.m4
rm -rf share/aclocal/printf-posix.m4
rm -rf share/aclocal/progtest.m4
rm -rf share/aclocal/size_max.m4
rm -rf share/aclocal/stdint_h.m4
rm -rf share/aclocal/uintmax_t.m4
rm -rf share/aclocal/visibility.m4
rm -rf share/aclocal/wchar_t.m4
rm -rf share/aclocal/wint_t.m4
rm -rf share/aclocal/xsize.m4

rm -rf share/dtds/legacy-icon-mapping.dtd

rm -rf share/gapi-2.0/atk-api.xml
rm -rf share/gapi-2.0/gdk-api.xml
rm -rf share/gapi-2.0/glade-api.xml
rm -rf share/gapi-2.0/glib-api.xml
rm -rf share/gapi-2.0/gtk-api.xml
rm -rf share/gapi-2.0/pango-api.xml

rm -rf share/glib-2.0/gettext

find share/locale -name 'atk10.mo' -delete
find share/locale -name 'gettext*' -delete
find share/locale -type d -empty -delete

rm -rf share/man/man1/autopoint.1
rm -rf share/man/man1/gdk-pixbuf-csource.1
rm -rf share/man/man1/gettext.1
rm -rf share/man/man1/gettextize.1
rm -rf share/man/man1/glib-genmarshal.1
rm -rf share/man/man1/glib-gettextize.1
rm -rf share/man/man1/glib-mkenums.1
rm -rf share/man/man1/gobject-query.1
rm -rf share/man/man1/gtester-report.1
rm -rf share/man/man1/gtester.1
rm -rf share/man/man1/gtk-builder-convert.1
rm -rf share/man/man1/gtk-query-immodules-2.0.1
rm -rf share/man/man1/msgattrib.1
rm -rf share/man/man1/msgcat.1
rm -rf share/man/man1/msgcmp.1
rm -rf share/man/man1/msgcomm.1
rm -rf share/man/man1/msgconv.1
rm -rf share/man/man1/msgen.1
rm -rf share/man/man1/msgexec.1
rm -rf share/man/man1/msgfilter.1
rm -rf share/man/man1/msgfmt.1
rm -rf share/man/man1/msggrep.1
rm -rf share/man/man1/msginit.1
rm -rf share/man/man1/msgmerge.1
rm -rf share/man/man1/msgunfmt.1
rm -rf share/man/man1/msguniq.1
rm -rf share/man/man1/ngettext.1
rm -rf share/man/man1/recode-sr-latin.1

rm -rf share/libgc-mono

rm -rf share/man/man3/bind_textdomain_codeset.3
rm -rf share/man/man3/bindtextdomain.3
rm -rf share/man/man3/dcgettext.3
rm -rf share/man/man3/dcngettext.3
rm -rf share/man/man3/dgettext.3
rm -rf share/man/man3/dngettext.3
rm -rf share/man/man3/gettext.3
rm -rf share/man/man3/libpng.3
rm -rf share/man/man3/libpngpf.3
rm -rf share/man/man3/ngettext.3
rm -rf share/man/man3/textdomain.3

rm -rf share/man/man5/png.5

rm -rf share/xml/libglade/*

# No debug files in the runtime
find . -name '*.mdb' -delete
