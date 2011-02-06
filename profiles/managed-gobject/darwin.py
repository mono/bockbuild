#!/usr/bin/python -B

import os
import sys

sys.path.append ('../..')

from bockbuild.darwinprofile import DarwinProfile

profile = DarwinProfile ()
profile.packages = [os.path.join ('..', '..', 'packages', p) for p in [
	'autoconf.py',
	'automake.py',
	'libtool.py',
	'gettext.py',
	'pkg-config.py',
	'mono.py',
	'glib.py',
	'libffi.py',
	'gobject-introspection.py'
]]
profile.build ()
