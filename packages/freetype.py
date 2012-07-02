SourceForgePackage ('%{name}', 'freetype', '2.4.9', override_properties = {
	'configure': './configure --prefix "%{prefix}"'
})
