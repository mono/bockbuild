class LibJpegTurboPackage (SourceForgePackage):
	def __init__ (self):
		SourceForgePackage.__init__(self,
			'%{name}',
			'libjpeg-turbo',
			'1.2.1'
			#override_properties = {
			#	'configure': './configure --prefix "%{prefix}"'
			#}
			)

LibJpegTurboPackage()

