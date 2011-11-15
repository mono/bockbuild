class GtkPackage (GnomePackage):
	def __init__ (self):
		GnomePackage.__init__ (self, 'gtk+',
			version_major = '2.24',
			version_minor = '7',
			configure_flags = [
				'--with-gdktarget=%{gdk_target}',
#				'--disable-cups',
			]
		)

		self.gdk_target = 'x11'
		if Package.profile.name == 'darwin':
			self.gdk_target = 'quartz'
			self.sources.extend ([
				# post-2.24.7 commits from 2.24 branch
				# gtkquartz: don't free the string returned by get_bundle_path()
				'http://git.gnome.org/browse/gtk+/patch/?id=c040b03c2e32a773a4d9cf4019050c2f8a5b91ce',
				# gtkrc.key.mac: remove half the file, it was an accidential double paste
				'http://git.gnome.org/browse/gtk+/patch/?id=79a92f99a9dbdc7b1a651b0e8665807bd89c6632',
				# gtkrc.key.mac: add Command-cursor text navigation
				'http://git.gnome.org/browse/gtk+/patch/?id=ccf12f7b406ecbd8f0c26b0e6dc86d4593144dab',
				# gtkrc.key.mac: add '"' missing from last commit
				'http://git.gnome.org/browse/gtk+/patch/?id=e81b6971d85c7a782269454311b022ce14787486',
				# Bug 662633 - Scheduled transaction editor crashes with gtk+-2.24.7
				'http://git.gnome.org/browse/gtk+/patch/?id=0a0fd5af99f2ae9b0f8cc6b943b98b7be43ed723',
				# quartz: remove unused variable
				'http://git.gnome.org/browse/gtk+/patch/?id=0f7c96b61936dd4796a6b33a04be3ac76f6f96fc',
				# quartz: Separate out screen_point conversion in function
				'http://git.gnome.org/browse/gtk+/patch/?id=cca1621e7117333ff6306b05e6508baab42e6210',
				# quartz: Factor out toplevel from NSEvent code into function
				'http://git.gnome.org/browse/gtk+/patch/?id=d0e5025694697c5f3394c2e94a58b343a13dc8c6',
				# quartz: Process motion events within windows bounds without window set
				'http://git.gnome.org/browse/gtk+/patch/?id=6725dee3aabc3335450657c5d40d54d6d217eeee',
				# quartz: make test_resize () conform to coding style
				'http://git.gnome.org/browse/gtk+/patch/?id=ff75900b5308f074184e5ebc793f3567da61a978',
				# quartz: make gdk_quartz_osx_version conform to coding style
				'http://git.gnome.org/browse/gtk+/patch/?id=5123ad079ea364a1083b579da92afc7415c0b8b7',
				# quartz: handle recursive CFRunLoops
				'http://git.gnome.org/browse/gtk+/patch/?id=6f4a6b4936c78b34682547de323b2afaf4559be6',
				# gdk: exclude MOD1 from the virtual modifier mapping
				'http://git.gnome.org/browse/gtk+/patch/?id=32b70a56d13050b6d2b0a570c436da1c303814f3',
				# [Quartz Bug 663182] NSImage throws an exception from _gtk_quartz_create_image_from_pixbuf()
				'http://git.gnome.org/browse/gtk+/patch/?id=fadc82ad2647277628fd140514b54473dbeb2f4c',

				# smooth scrolling, https://bugzilla.gnome.org/show_bug.cgi?id=516725
				'http://bugzilla-attachments.gnome.org/attachment.cgi?id=200174',

				# make new modifier behviour opt-in, so as not to break old versions of MonoDevelop
				'patches/gdk-quartz-set-fix-modifiers-hack.patch',
			])

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

GtkPackage ()
