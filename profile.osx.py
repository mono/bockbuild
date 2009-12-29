profile = {
	'name':         'osx',
	'build_root':   os.path.join (os.getcwd (), 'build-root'),
	'prefix':       '%{build_root}/_install',
	'mac_sdk_path': '/Developer/SDKs/MacOSX10.5.sdk',
}

if not os.path.isdir (profile['mac_sdk_path']):
	sys.exit ('Mac OS X SDK does not exist: %s' % profile['mac_sdk_path'])

gcc_arch_flags = [ '-m32', '-arch i386' ]
gcc_flags = [
	'-D_XOPEN_SOURCE',
	'-isysroot %{mac_sdk_path}',
	'-mmacosx-version-min=10.5',
	'-I%{prefix}/include'
]
gcc_flags.extend (gcc_arch_flags)

profile['environ'] = {
	'PATH':            '%{prefix}/bin:/usr/bin:/bin',

	'CC':              'gcc-4.2',
	'CXX':             'g++-4.2',
	'CFLAGS':          ' '.join (gcc_flags),
	'CXXFLAGS':        '%{CFLAGS}',
	'CPPFLAGS':        '%{CFLAGS}',
	'C_INCLUDE_PATH':  '%{prefix}/include',

	'LD_LIBRARY_PATH': '%{prefix}/lib',
	'LDFLAGS':         '-L%{prefix}/lib ' + ' '.join (gcc_arch_flags),

	'ACLOCAL_FLAGS':   '-I%{prefix}/share/aclocal',

	'PKG_CONFIG_PATH': '%{prefix}/lib/pkgconfig:%{prefix}/share/pkgconfig'
}

profile['packages'] = [
	# Base dependencies
	'packages/autoconf.py',
	'packages/automake.py',
	'packages/libtool.py',
	'packages/gettext.py',
	'packages/pkg-config.py',
	'packages/libiconv.py',
	'packages/libpng.py',
	'packages/libjpeg.py',
	'packages/freetype.py',
	'packages/fontconfig.py',
	'packages/pixman.py',
	'packages/cairo.py',
	'packages/glib.py',
	'packages/pango.py',
	'packages/atk.py',
	'packages/intltool.py',
	'packages/gtk+.py',
	'packages/libxml2.py',
	'packages/libglade.py',
	'packages/libproxy.py',
	'packages/libsoup.py',
	'packages/sqlite.py',
	'packages/ige-mac-integration.py',
	'packages/mono.py',

	# Icons
	'packages/librsvg.py',
	'packages/icon-naming-utils.py',
	'packages/hicolor-icon-theme.py',
	'packages/tango-icon-theme.py',

	# Xiph codecs/formats
	'packages/libogg.py',
	'packages/libvorbis.py',
	'packages/flac.py',
	'packages/libtheora.py',
	'packages/speex.py',

	# Various formats
	'packages/wavpack.py',
	'packages/taglib.py',

	# GStreamer
	'packages/liboil.py',
	'packages/gstreamer.py',
	'packages/gst-plugins-base.py',
	'packages/gst-plugins-good.py',
	'packages/gst-plugins-bad.py',
	'packages/gst-plugins-ugly.py',

	# Managed Deps
	'packages/gtk-sharp.py',
	'packages/mono-addins.py',
	'packages/ndesk-dbus.py',
	'packages/ndesk-dbus-glib.py',
	'packages/taglib-sharp.py',
	'packages/ige-mac-integration-sharp.py',

	'packages/banshee.py'
]
