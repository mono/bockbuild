SourceForgePackage ('%{name}', 'freetype', '2.5.0.1', override_properties = {
	'configure': './configure --prefix "%{prefix}"'
})
