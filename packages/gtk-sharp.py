Package ('gtk-sharp', '2-12-branch',
	sources = [ 'git@github.com:mono/gtk-sharp.git' ],
	revision = '98e9439afa4b4da7cd2f3d1ab92b6415ab50b01d',
	override_properties = { 'configure':
		'./bootstrap-2.12 --prefix="%{prefix}"'
	})
