package = {
	'name':    'gst-plugins-ugly',
	'version': '0.10.13',
	'sources': [
		'http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure}' \
			' --disable-gtk-doc' \
			' --disable-asfdemux' \
			' --disable-dvdsub' \
			' --disable-dvdlpcmdec' \
			' --disable-iec958' \
			' --disable-mpegstream' \
			' --disable-realmedia',
		'%{__make}'
	]
}
