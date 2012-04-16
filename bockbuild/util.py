import re
import glob
import os
import sys
import subprocess
import fileinput

def log (level, message):
	if level == 0:
		print '==> %s' % message
	elif level == 1:
		print '    + %s' % message
	elif level == 2:
		print '      - %s' % message

def expand_macros (node, vars):
	def sub_macro (m):
		type = m.groups ()[0]
		expr = m.groups ()[1]
		if type == '%':
			expr = 'self.' + expr
		o = eval (expr, {}, { 'self': vars })
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
	if print_cmd: print cmd
	proc = subprocess.Popen (cmd, shell = True)
	exit_code = os.waitpid (proc.pid, 0)[1]
	if not exit_code == 0:
		print
		sys.exit ('ERROR: command exited with exit code %s: %s' % (exit_code, cmd))

def backtick (cmd):
	lines = []
	for line in os.popen (cmd).readlines ():
		lines.append (line.rstrip ('\r\n'))
	return lines

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
