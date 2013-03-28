SourceForgePackage ('%{name}', 'freetype', '2.4.11', override_properties = {
	'configure': './configure --prefix "%{prefix}"'
})
