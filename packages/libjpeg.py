package = {
	'name':    'libjpeg',
	'version': '7',
	'sources': [
		'http://www.ijg.org/files/jpegsrc.v%{version}.tar.gz'
	],
	'prep': [
		'tar xf @{sources:0}',
		'cd jpeg-%{version}'
	]
}
