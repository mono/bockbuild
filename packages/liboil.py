Package ('liboil', '0.3.16',
	sources = [
		'http://download.banshee-project.org/misc/%{name}-%{version}.tar.gz'
		# a bunch of liboil releases appear to be missing from the site...
		# 'http://%{name}.freedesktop.org/download/%{name}-%{version}.tar.gz'
	],
	configure_flags = [
		'--disable-gtk-doc'
	]
)
