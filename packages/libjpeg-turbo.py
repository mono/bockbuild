class LibJpegTurboPackage (SourceForgePackage):
	def __init__ (self):
		SourceForgePackage.__init__(self,
			'%{name}',
			'libjpeg-turbo',
			'1.3.0'
			#override_properties = {
			#	'configure': './configure --prefix "%{prefix}"'
			#}
			)

		if Package.profile.name == "darwin" and Package.profile.m64:
			self.configure_flags.extend ([ '--host x86_64-apple-darwin' ])

LibJpegTurboPackage()

