package = {
	'name':    'gstreamer',
	'version': '0.10.25',
	'sources': [
		'http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure}' \
			' --disable-gtk-doc',
		'%{__make}'
	]
}
