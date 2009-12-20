package = {
	'name':    'gst-plugins-good',
	'version': '0.10.17',
	'sources': [
		'http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure}' \
			' --disable-gtk-doc' \
			' --disable-x' \
			' --disable-xvideo' \
			' --disable-xshm' \
			' --disable-gdk_pixbuf' \
			' --disable-cairo' \
			' --disable-jpeg' \
			' --disable-libpng' \
			' --disable-annodex',
		'%{__make}'
	]
}
