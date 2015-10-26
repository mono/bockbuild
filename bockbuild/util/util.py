import re
import glob
import os
import sys
import subprocess
import fileinput
import inspect
import time
import difflib
import shutil
import tarfile
import hashlib
import stat

# from https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class config:
	trace = False
	filter = None # function name/package name filter for trace() and test()
	test = False
	iterative = False # FIXME: this needs a bit more work
	quiet = None
	never_rebuild = False
	verbose = False

class CommandException (Exception): # shell command failure
	def __init__ (self, message):
		Exception.__init__ (self, '%s: %s (path: %s)' % (get_caller(), os.getcwd (), message))
		verbose (message)

class BockbuildException (Exception): # internal/unexpected issue, treat as unrecoverable
	def __init__ (self, message):
		Exception.__init__ (self, message)

def log (phase, message):
	#DISABLED until we can properly refactor/redirect logging
	return

#TODO: move these functions to either Profile or their own class

def get_caller (skip = 0, get_dump = False):
	#this whole thing fails if we're not in a valid directory
	try:
		cwd = os.getcwd ()
	except OSError as e:
		return '~could not get caller (current directory not valid)~'

	stack = inspect.stack (3)
	if len (inspect.stack()) < 3 + skip:
		return 'top'
	output = None
	last_caller = None
	for record in stack [2 + skip:]:
		caller = record[3]
		frame = record[0]

		try:
			if 'self' in frame.f_locals:
				try:
					output = '%s->%s' % (frame.f_locals['self'].name, caller)
				except Exception as e:
					pass
				finally:
					if output == None:
						output = '%s->%s' % (frame.f_locals['self'].__class__.__name__, caller)
			else:
				last_caller = caller
			if get_dump:
				output = output + "\n" + "\t".join(dump (frame.f_locals['self'], 'self'))

		except Exception as e:
			pass
		if output != None:
			return output

	if output == None:
		return last_caller

def assert_exists (path):
	if not os.path.exists (path):
		error ('assert_exists failed: ' + os.path.basename (path))

def loginit (message):
	if os.getenv ('BUILD_REVISION') is not None:  #MonkeyWrench
		print '@MonkeyWrench: SetSummary:<h3>%s</h3>' % message
	else:
		logprint (message, bcolors.BOLD)

def logprint (message, color, summary = False, trace = False):
	if config.quiet == True and trace == False:
		return
	if summary:
		if os.getenv ('BUILD_REVISION') is not None:  #MonkeyWrench
				print '@MonkeyWrench: AddSummary:<p>%s</p>' % message
				return

	message = '%s%s%s' % ('\n', message, '\n')
	if sys.stdout.isatty():
		print '%s%s%s' % (color, message , bcolors.ENDC)
	else:
		print message

def title (message, summary = True):
	logprint ('** %s **' % message, bcolors.HEADER, summary)

def info (message, summary = True):
	logprint (message ,bcolors.OKGREEN, summary)

def progress (message):
	logprint ('%s: %s' % (get_caller (), message), bcolors.OKBLUE)

def verbose (message):
	if not config.verbose and not config.trace:
		return
	logprint ('%s: %s' % (get_caller (), message), bcolors.OKBLUE)

def warn (message):
	logprint ('(bockbuild warning) %s: %s' % (get_caller (), message), bcolors.FAIL)

def error (message, more_output = False):
	def expand (message):
			for k in message.keys ():
				if isinstance (message [k], (str, list, tuple, dict, bool, int)) and not k.startswith ('_'):
					yield '%s: %s\n' % (k, message [k])

	if isinstance (message, dict):
		message = "\n".join (expand (message))
	config.trace = False
	header = '(bockbuild error)' if not more_output else ''
	if isinstance (message, CommandException):
		logprint ('%s: %s' % (header, message) , bcolors.FAIL, summary = True)
	else:
		logprint ('%s %s: %s' % (header, get_caller (), message) , bcolors.FAIL, summary = True)
	if not more_output:
		sys.exit (255)

def trace (message, skip = 0):
	if config.trace == False:
		return

	caller = get_caller(skip)

	if config.filter != None and config.filter not in caller:
		return

	logprint ('%s: %s' % (caller, message), bcolors.FAIL, summary = True, trace = True)

def test (func):
	if config.test == False:
		return
	caller = get_caller ()

	if config.filter != None and config.filter not in caller:
		return

	if func() == False:
		error ('Test ''%s'' failed.' % func.__name__)

def retry (func, tries = 3, delay = 5):
	result = None
	exc = None
	cwd = os.getcwd ()
	result = None
	for x in range(tries):
		try:
			os.chdir (cwd)
			result = func ()
			break
		except CommandException as e:
			if x == tries - 1:
				error (str(e))
			info (str(e))
			info ("Retrying ''%s'' in %s secs" % (func.__name__, delay))
			time.sleep (delay)

	return result


def ensure_dir (d, purge = False):
	if os.path.exists(d):
		if purge == True:
			trace ('Nuking %s' % d)
			unprotect_dir (d, recursive = True)
			delete (d)
		else: return
	os.makedirs (d)

def identical_files (first, second): # quick and dirty assuming they have the same name/paths
	hash1 = hashlib.sha1(open(first).read()).hexdigest()
	hash2 = hashlib.sha1(open(second).read()).hexdigest()

	return hash1 == hash2

def md5 (path):
	return hashlib.md5 (open (path).read ()).hexdigest ()

def update (new_text, file, show_diff = True):
	orig_text = None
	if os.path.exists (file):
		orig_text = open (file).readlines ()

	output = open (file, 'w')
	output.writelines (new_text)

	if orig_text == None:
		return False

	difflines = [line for line in difflib.context_diff(orig_text, new_text, n=0)]
	if len (difflines) > 0:
		if show_diff == True:
			brieflines = [line.rstrip('\r\n') for line in difflines if line.startswith(('+ ','- ','! '))]
			info ('\n'.join (brieflines))
		return True # changes
	else:
		return False

def get_filetype (path):
	# the env variables are to work around a issue with OS X and 'file': https://trac.macports.org/ticket/38771
	return backtick ('LC_CTYPE=C LANG=C file -b "%s"' % path)[0]


def find_git(self):
        self.git = 'git'
        for git in ['/usr/local/bin/git', '/usr/local/git/bin/git', '/usr/bin/git']:
			if os.path.isfile (git):
				self.git = git
				break

def assert_git_dir(self):
	if (os.system(expand_macros ('%{git} rev-parse HEAD > /dev/null', self))) != 0:
		raise Exception('assert_git_dir')

def git_get_revision(self):
	assert_git_dir(self)
	return backtick (expand_macros ('%{git} rev-parse HEAD', self))[0]

def git_get_branch(self):
	assert_git_dir(self)
	revision = git_get_revision (self)
	output = backtick (expand_macros ('%{git} symbolic-ref -q --short HEAD', self))
	if len(output) == 0:
		return None #detached HEAD
	else: return output[0]

def git_is_dirty(self):
	assert_git_dir(self)
	str = backtick (expand_macros ('%{git} symbolic-ref --short HEAD --dirty', self))[0]
	return 'dirty' in str

def git_patch (self, dir, patch):
	assert_git_dir(self)
	run_shell (expand_macros ('%' + '{git} diff > %s', self))

def git_shortid (self):
	assert_git_dir(self)
	branch = git_get_branch (self)
	short_rev = backtick (expand_macros ('git describe --abbrev --always --dirty', self))[0]
	if branch == None:
		return  short_rev
	else:
		return '%s-%s' % (branch, short_rev)

def protect_dir (dir, recursive = False):
	if not recursive:
		os.chmod (dir, stat.S_IRUSR | stat.S_IXUSR)
	else:
		for root,subdirs,filelist in os.walk (dir):
			protect_dir (root, recursive = False)

def unprotect_dir (dir, recursive = False):
	if not recursive:
		os.chmod (dir, stat.S_IRUSR | stat.S_IXUSR | stat.S_IWUSR | stat.S_IXGRP | stat.S_IRGRP | stat.S_IXOTH | stat.S_IROTH)
	elif os.path.isdir (dir):
		for root,subdirs,filelist in os.walk (dir):
			unprotect_dir (root, recursive = False)

def delete (path):
	if not os.path.isabs (path):
		raise BockbuildException ('Relative paths are not allowed.')

	if not os.path.exists (path):
		raise CommandException ('Invalid path to rm: %s' % path)

	def rmtree ():
		try:
			unprotect_dir (path, recursive = True)
			if os.path.isfile (path) or os.path.islink (path):
				os.remove (path)
			elif os.path.isdir (path):
				shutil.rmtree (path, ignore_errors=False)
		except OSError as e:
			if os.path.exists (path):
				raise # It's still there, so we try again

	#retry (rmtree, tries = 5, delay = 1)
	rmtree ()

def merge_trees(src, dst, delete_src = True):
	if not os.path.isdir(src) or not os.path.isdir(dst):
		raise Exception ('"%s" or "%s" are not both directories ' % (src, dst))
	run_shell('rsync -a --ignore-existing %s/* %s' % (src, dst), False)
	if delete_src:
		delete (src)

def iterate_dir (dir, with_links = False, with_dirs = False, summary = False):
	x = 0
	links = 0
	dirs = 0

	for root,subdirs,filelist in os.walk (dir):
		dirs = dirs + 1
		if with_dirs:
			yield root
		for file in filelist:
			path = os.path.join (root, file)
			if os.path.islink (path):
				links = links + 1
				if with_links:
					yield path
				continue
			x = x + 1
			yield path

	if summary:
		info ("%s: %s files, %s dirs, %s symlinks" % (os.path.relpath(dir, os.getcwd()), x, dirs, links))

def zip (src, archive):
	x = 0
	# thanks to http://stackoverflow.com/a/17080988

	pwd = os.getcwd()

	try:
		os.chdir (src)
		with tarfile.open(archive, "w:gz") as zip:
			for path in iterate_dir (src, with_links = True, with_dirs = True, summary = False):
				relpath = os.path.relpath (path, src)
				zip.add(relpath, recursive = False)
				x = x + 1
	finally:
		os.chdir (pwd)

def unzip (archive, dst):
	if os.path.exists (dst):
		raise Exception ('unzip: Destination should not exist: %s' % dst)

	pwd = os.getcwd()
	relroot = os.path.abspath(os.path.join(dst, os.pardir))

	try:
		os.chdir(relroot)
		with tarfile.open(archive) as zip:
			zip.extractall (dst)
	except:
		if os.path.exists (archive):
			delete (archive)
		if os.path.exists (dst):
			delete (dst)
		raise
	finally:
		os.chdir(pwd)

def dump (self, name):
	for k in self.__dict__.keys ():
		if isinstance (self.__dict__[k], (str, list, tuple, dict, bool, int)) and not k.startswith ('_'):
			yield '%s.%s = "%s"\n' % (name, k, self.__dict__[k])

def expand_macros (node, vars, extra_vars = None):
	def sub_macro (m):
		type = m.groups ()[0]
		expr = m.groups ()[1]
		if type == '%':
			expr = 'self.' + expr

		resolved = False
		for var in [vars, extra_vars]:
			try:
				o = eval (expr, {}, { 'self': var })
				resolved = True
				break
			except:
				pass
		if not resolved:
			error ("'%s' could not be resolved in string '%s'" % (m.groups ()[1], node))
		if o == None:
			return ''
		elif isinstance (o, (list, tuple)):
			return ' '.join (o)
		return str (o)

	if hasattr (node, '__dict__'):
		for k, v in node.__dict__.iteritems ():
			if not k.startswith ('_'):
				node.__dict__[k] = expand_macros (v, vars)
	elif isinstance (node, dict):
		for k, v in node.iteritems ():
			node[k] = expand_macros (v, vars)
	elif isinstance (node, (list, tuple)):
		for i, v in enumerate (node):
			node[i] = expand_macros (v, vars)
	elif isinstance (node, str):
		orig_node = node
		iters = 0
		while True:
			v = re.sub ('(?<!\\\)([%$]){([^}]+)}',
				sub_macro, node)
			if v == node:
				break
			iters += 1
			if iters >= 500:
				sys.exit ('Too many macro substitutions, possible recursion:'
					'\'%s\'' % orig_node)
			node = v

	return node

def replace_in_file(filename, word_dic):
	rc = re.compile('|'.join(map(re.escape, word_dic)))
	def translate(match):
		return word_dic[match.group(0)]
	for line in fileinput.FileInput(filename, inplace=1):
		print rc.sub(translate, line)

def run_shell (cmd, print_cmd = False):
	if print_cmd: print '++',cmd
	if not print_cmd: trace (cmd)
	proc = subprocess.Popen (cmd, shell = True, bufsize = -1)
	exit_code = proc.wait ()
	if not exit_code == 0:
		raise CommandException('"%s" failed, error code %s' % (cmd, exit_code))

def backtick (cmd, print_cmd = False):
	if print_cmd: print '``', cmd
	if not print_cmd: trace (cmd)
	proc = subprocess.Popen (cmd, shell = True, bufsize = -1, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	stdout, stderr = proc.communicate ()

	exit_code = proc.returncode

	if not exit_code == 0:
		raise CommandException('"%s" failed, error code %s\nstderr:\n%s' % (cmd, exit_code, stderr))

	return stdout.split ('\n')

def get_host ():
	search_paths = ['/usr/share', '/usr/local/share']
	am_config_guess = []
	for path in search_paths:
		am_config_guess.extend (glob.glob (os.path.join (
			path, os.path.join ('automake*', 'config.guess'))))
	for config_guess in am_config_guess:
		config_sub = os.path.join (os.path.dirname (config_guess), 'config.sub')
		if os.access (config_guess, os.X_OK) and os.access (config_sub, os.X_OK):
			return backtick ('%s %s' % (config_sub, backtick (config_guess)[0]))[0]
	return 'python-%s' % os.name

def get_cpu_count ():
	try:
		return os.sysconf ('SC_NPROCESSORS_CONF')
	except:
		return 1
