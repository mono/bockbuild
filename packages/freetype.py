package = {
	'name':    'freetype',
	'version': '2.3.11',
	'sources': [
		'http://downloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz'
	],
	'build': [
		'./configure --prefix %{_prefix}',
		'%{__make}'
	]
}
