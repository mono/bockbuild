FreeDesktopPackage ('%{name}', 'pkg-config', '0.27', configure_flags = [ "--with-internal-glib" ], override_properties = { 'build_dependency' : True })
