class MonoMacPackage (Package):
	def __init__ (self):
		self.pkgconfig_version = '0.7'
		self.maccore_tag = 'monomac-0-6'
		self.maccore_source_dir_name = 'mono-maccore-9c54c33'
		self.monomac_tag = 'monomac-0-7'
		self.monomac_source_dir_name = 'mono-monomac-3a2c2f6'	
		
		Package.__init__ (self, 'monomac', self.monomac_tag)
		
		self.sources = [
			'https://github.com/mono/maccore/tarball/%{maccore_tag}',
			'https://github.com/mono/monomac/tarball/%{monomac_tag}'
		]

	def prep (self):
		self.sh ('tar xf "%{sources[0]}"')
		self.sh ('tar xf "%{sources[1]}"')
		self.sh ('mv %{maccore_source_dir_name} maccore')
		self.sh ('mv %{monomac_source_dir_name} monomac')
		self.cd ('monomac/src')
	
	def build (self):
		self.sh ('make')

	def install (self):
		self.sh ('mkdir -p %{prefix}/lib/monomac')
		self.sh ('mkdir -p %{prefix}/share/pkgconfig')
		self.sh ('echo "Name: MonoMac\nDescription: Mono Mac bindings\nVersion:%{pkgconfig_version}\nLibs: -r:%{prefix}/lib/monomac/MonoMac.dll" > %{prefix}/share/pkgconfig/monomac.pc')
		self.sh ('cp MonoMac.dll %{prefix}/lib/monomac')

MonoMacPackage ()
