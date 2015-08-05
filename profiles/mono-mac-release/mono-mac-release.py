#!/usr/bin/python -B -u
import sys 
import traceback

sys.path.append('../..')

from MonoReleaseProfile import MonoReleaseProfile
from bockbuild.util.util import *

try:
	MonoReleaseProfile().build()
except Exception as e:
	exc_type, exc_value, exc_traceback = sys.exc_info()
	error ('%s\n%s' % (str(e), repr(traceback.extract_tb(exc_traceback))))
