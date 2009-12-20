package = {
	'name':    'gst-plugins-bad',
	'version': '0.10.17',
	'sources': [
		'http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure}' \
			' --disable-gtk-doc' \
			' --with-plugins=quicktime' \
			' --disable-apexsink' \
			' --disable-bz2' \
			' --disable-metadata' \
			' --disable-oss4' \
			' --disable-theoradec',
		'%{__make}'
	]
}
