profile = {
	'name': 'linux',
	'build_root': os.path.join (os.getcwd (), 'build-root'),
	'prefix': '%{build_root}/_install',
}

search_paths = ['%{prefix}']
bin_paths = [os.path.join (p, 'bin') for p in search_paths]
bin_paths.extend (['/usr/bin', '/bin'])
lib_paths = [os.path.join (p, 'lib') for p in search_paths]
aclocal_paths = [os.path.join (p, 'share', 'aclocal') for p in search_paths]

profile['environ'] = {
	'PATH': ':'.join (bin_paths),
	'LD_LIBRARY_PATH': ':'.join (lib_paths),
	'LDFLAGS': ' '.join (['-L' + p for p in lib_paths]),
	'ACLOCAL_FLAGS': ' '.join (['-I' + p for p in aclocal_paths]),
	'PKG_CONFIG_PATH': ':'.join ([
		os.path.join (p, d, 'pkgconfig')
			for p in search_paths
			for d in ['lib', 'share'] 
	])
}

profile['packages'] = [
	# Base dependencies
	'packages/libxml2.py',
	'packages/libproxy.py',
	'packages/intltool.py',
	'packages/libsoup.py',
	
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
	'packages/ndesk-dbus.py',
	'packages/ndesk-dbus-glib.py',
	'packages/taglib-sharp.py',
	'packages/ige-mac-integration-sharp.py'
]
