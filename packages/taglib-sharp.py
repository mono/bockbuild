package = {
	'name':    'taglib-sharp',
	'version': '2.0.3.3',
	'sources': [
		'http://download.banshee-project.org/%{name}/%{version}/%{name}-%{version}.tar.gz'
	],
	'build': [
		'%{__configure}' \
			' --disable-docs',
		'%{__make}'
	]
}
