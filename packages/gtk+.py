class GtkPackage (GnomePackage):
	def __init__ (self):
		GnomePackage.__init__ (self, 'gtk+',
			version_major = '2.24',
			version_minor = '5',
			configure_flags = [
				'--with-gdktarget=%{gdk_target}',
#				'--disable-cups',
			]
		)

		self.gdk_target = 'x11'
		if Package.profile.name == 'darwin':
			self.gdk_target = 'quartz'
			self.sources.extend ([
				#patches from gtk-osx-build
				'patches/gtk/gtkselection.patch',
				'patches/gtk/gdkwindow-quartz.patch',
				'patches/gtk/gtk-keyhash.patch',
				'patches/gtk/gtk-relocation.patch',
				'patches/gtk/gdk-deadkeys.patch',
				'patches/gtk/gdkeventloop.patch',
				'patches/gtk/gtkdndmemory.patch',
				'patches/gtk/gtkselection_deref.patch',

				# Bug 346609 - [PATCH] Quartz backend has no support for one-button mice
				#https://bugzilla.gnome.org/show_bug.cgi?id=346609
				'patches/gtk/gtkcontrolclick.patch',

				# Bug 655074 - [PATCH] Fix crash with undecorated windows on MacOS Lion
				#https://bugzilla.gnome.org/show_bug.cgi?id=655074
				'patches/gtk/gtkundecoratedwindow.patch',

				# add some missing keybindings
				'patches/gtk/gtkmackeys.patch',

				# Bug 655122 - Crash when resizing window on MacOS Lion
				# https://bugzilla.gnome.org/show_bug.cgi?id=655122
				'patches/gtk/gtklionresizecrash.patch',

				# Bug 655087 - CoreGraphics error "clip: empty path" creating
				# new window on Lion
				# https://bugzilla.gnome.org/show_bug.cgi?id=655087
				'patches/gtk/gdkemptypath.patch',
			])

	def prep (self):
		Package.prep (self)
		if Package.profile.name == 'darwin':
			for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

GtkPackage ()
