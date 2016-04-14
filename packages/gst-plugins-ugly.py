GstreamerPackage('gstreamer', 'gst-plugins-ugly', '0.10.19', configure_flags=[
    ' --disable-gtk-doc',
    ' --disable-asfdemux',
    ' --disable-dvdsub',
    ' --disable-dvdlpcmdec',
    ' --disable-iec958',
    ' --disable-mpegstream'
    ' --disable-realmedia'
])
