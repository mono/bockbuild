#!/usr/bin/python -B -u
import sys 

sys.path.append('../..')

from MonoReleaseProfile import MonoReleaseProfile
from bockbuild.util.util import *

try:
	MonoReleaseProfile().build()
except e as Exception:
	error (str(e))
	raise
