package = {
	'name':    'gst-plugins-base',
	'version': '0.10.25',
	'sources': [
		'http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure}' \
			' --disable-gtk-doc' \
			' --disable-x' \
			' --disable-xvideo' \
			' --disable-xshm' \
			' --disable-gio' \
			' --disable-gnome_vfs',
		'%{__make}'
	]
}
