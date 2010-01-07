# FIXME version is out of date from upstream, but GStreamer lost all
# their tarballs, so falling back to the tarball from openSUSE,
# which is also very out of date... should be 0.10.13
GstreamerPackage ('gstreamer', 'gst-plugins-ugly', '0.10.12', configure_flags = [
	' --disable-gtk-doc',
	' --disable-asfdemux',
	' --disable-dvdsub',
	' --disable-dvdlpcmdec',
	' --disable-iec958',
	' --disable-mpegstream'
	' --disable-realmedia'
])
