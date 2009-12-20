package = {
	'name':    'mono-addins',
	'version': '0.4',
	'sources': [
		'http://ftp.novell.com/pub/mono/sources/%{name}/%{name}-%{version}.zip'
	],
	'prep': [
		'unzip @{sources:0}',
		'cd %{name}-%{version}'
	],
	'build': [
		'%{__configure} --disable-gui',
		'%{__make}'
	]
}
