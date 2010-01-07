SourceForgePackage ('%{name}', 'freetype', '2.3.11', override_properties = {
	'configure': './configure --prefix %{prefix}'
})
