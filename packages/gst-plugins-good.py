configure_flags = [
	'--disable-gtk-doc',
	'--disable-gdk_pixbuf',
	'--disable-cairo',
	'--disable-jpeg',
	'--disable-libpng',
	'--disable-annodex'
]

# FIXME: these should be passed on the Linux profile
# when we do away with xvideo/xoverlay and replace
# with Clutter and Cairo
if profile['name'] == 'osx':
	configure_flags.extend ([
		'--disable-x',
		'--disable-xvideo',
		'--disable-xshm'
	])

package = {
	'name':    'gst-plugins-good',
	'version': '0.10.17',
	'sources': [
		'http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.gz'
	],
	'build': [
		'CFLAGS=-I%{_prefix}/include %{__configure} ' + ' '.join (configure_flags),
		'CFLAGS=-I%{_prefix}/include %{__make}'
	]
}
