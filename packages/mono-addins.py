Package ('mono-addins', '0.4',
	sources = [ 'http://ftp.novell.com/pub/mono/sources/%{name}/%{name}-%{version}.zip' ],
	override_properties = { 'make': 'make' }
)
