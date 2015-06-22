class PangoPackage (GnomeXzPackage):
	def __init__ (self):
		GnomePackage.__init__ (self,
			'pango',
			version_major = '1.35',
			version_minor = '0',
			configure_flags = [
				'--without-x',
			]
		)

		default_patch_options = '-p1'

		if Package.profile.name == 'darwin':
			self.sources.extend ([
				# 1
				# Bug 321419 - Allow environment var substitution in Pango config
				# https://bugzilla.gnome.org/show_bug.cgi?id=321419
				Patch('patches/pango-relative-config-file.patch', options = default_patch_options),

				# BXC 10257 - Characters outside the Basic Multilingual Plane don't render correctly
				# https://bugzilla.xamarin.com/show_bug.cgi?id=10257
				Patch('patches/pango-coretext-astral-plane-1.patch', options = default_patch_options),
				Patch('patches/pango-coretext-astral-plane-2.patch', options = default_patch_options),

				# Bug 15787 - Caret position is wrong when there are ligatures
				# https://bugzilla.xamarin.com/show_bug.cgi?id=15787
				Patch('patches/pango-disable-ligatures.patch', options = default_patch_options),

				# https://bugzilla.xamarin.com/show_bug.cgi?id=22199
				Patch('patches/pango-fix-ct_font_descriptor_get_weight-crasher.patch', options = default_patch_options),

				# https://bugzilla.gnome.org/show_bug.cgi?id=734372
				Patch('patches/pango-coretext-condensed-trait.patch', options = default_patch_options), 
			])

PangoPackage ()
