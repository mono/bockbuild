Package ('gtk-sharp', '2-12-branch',
	sources = [ 'git@github.com:mono/gtk-sharp.git' ],
	revision = '36e3f5b803ec8c7761910a278669594c76582b8b',
	override_properties = { 'configure':
		'./bootstrap-2.12 --prefix="%{prefix}"'
	})
