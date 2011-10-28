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
				'patches/gtk/01-c040b03c2e32a773a4d9cf4019050c2f8a5b91ce.patch',
				# gtkrc.key.mac: remove half the file, it was an accidential double paste
				'patches/gtk/02-79a92f99a9dbdc7b1a651b0e8665807bd89c6632.patch',
				# gtkrc.key.mac: add Command-cursor text navigation
				'patches/gtk/03-ccf12f7b406ecbd8f0c26b0e6dc86d4593144dab.patch',
				# gtkrc.key.mac: add '"' missing from last commit
				'patches/gtk/04-e81b6971d85c7a782269454311b022ce14787486.patch',

				# https://bugzilla.gnome.org/show_bug.cgi?id=516725
				# http://bugzilla-attachments.gnome.org/attachment.cgi?id=197616
				'patches/gtk/gtk-smooth-scrolling.patch',
			])

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

GtkPackage ()
