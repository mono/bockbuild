class LibGdiPlusPackage (GitHubPackage):
	def __init__ (self):
		GitHubPackage.__init__ (self, 'mono', 'libgdiplus', '2.11', 'b2fd6394f5604f2f6de66f07935b64ed575af48c',
			configure = './autogen.sh --prefix="%{prefix}"')

		self.sources.extend ([
			'patches/libgdiplus-libpng15.patch',
		])

	def prep (self):
		Package.prep (self)
		for p in range (1, len (self.sources)):
			self.sh ('patch -p1 --ignore-whitespace < "%{sources[' + str (p) + ']}"')

LibGdiPlusPackage ()
