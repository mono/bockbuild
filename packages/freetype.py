SourceForgePackage ('%{name}', 'freetype', '2.4.3', override_properties = {
	'configure': './configure --prefix "%{prefix}"'
})
