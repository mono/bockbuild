Package ('gtk-sharp', '2-12-branch',
	sources = [ 'git@github.com:mono/gtk-sharp.git' ],
	revision = 'acbb04600d2dbdbe889117c07ee660818abd7070',
	override_properties = { 'configure':
		'./bootstrap-2.12 --prefix="%{prefix}"'
	})
