SourceForgePackage ('%{name}', 'freetype', '2.4.2', override_properties = {
	'configure': './configure --prefix "%{prefix}"'
})
