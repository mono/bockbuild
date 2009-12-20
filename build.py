#!/usr/bin/env python

import os
import sys
import re
import glob
import shutil
import urllib
import subprocess
from optparse import OptionParser

def build_package (profile, (package, vars)):
	package_dir = os.path.dirname (package['_path'])
	package_build_dir = os.path.join (profile['build_root'],
		'%s-%s' % (package['name'], package['version']))
	build_success_file = os.path.join (profile['build_root'],
		'%s-%s.success' % (package['name'], package['version']))

	if os.path.exists (build_success_file):
		print 'Skipping %s - already built' % package['name']
		return

	print 'Building %s on %s (%s CPU)' % (package['name'], profile['host'], profile['cpu_count'])

	# Set up the directories
	if not os.path.exists (profile['build_root']) or not os.path.isdir (profile['build_root']):
		os.makedirs (profile['build_root'], 0755)

	shutil.rmtree (package_build_dir, ignore_errors = True)
	os.makedirs (package_build_dir)

	# Copy/download sources into the build root, and adjust the
	# sources list in the package object to be relative local
	# filenames from the build root directory for later
	log (0, 'Retrieving sources')
	local_sources = []
	for source in package['sources']:
		source = expand_macros (source, vars)
		local_source = os.path.join (package_dir, source)
		local_source_file = os.path.basename (local_source)
		local_sources.append (local_source_file)
		local_dest_file = os.path.join (package_build_dir, local_source_file)

		if os.path.isfile (local_source):
			log (1, 'copying local source: %s' % local_source_file)
			shutil.copy2 (local_source, local_dest_file)
		elif source.startswith (('http', 'https', 'ftp')):
			log (1, 'downloading remote source: %s' % source)
			urllib.urlretrieve (source, local_dest_file)

	package['sources'] = local_sources
	
	os.chdir (package_build_dir)

	for phase in ['prep', 'build', 'install']:
		log (0, '%sing %s' % (phase.capitalize (), package['name']))
		for step in package[phase]:
			step = expand_macros (step, package)
			log (1, step)
			if step.startswith ('cd '):
				os.chdir (step[3:])
			else:
				if not profile['verbose']:
					step = '( %s ) &>/dev/null' % step
				run_shell (step)

	open (build_success_file, 'w').close ()

def load_package_defaults (profile, package):
	# path macros
	package['_build_root'] = os.path.join (profile['build_root'], '_install')
	package['_prefix'] = package['_build_root']

	# tool macros
	package['__configure'] = './configure --prefix=%{_prefix}'
	package['__make'] = 'make -j%s' % profile['cpu_count']
	package['__makeinstall'] = '%{__make} install'

	# install default sections if they are missing
	package.setdefault ('prep', ['tar xf @{sources:0}', 'cd %{name}-%{version}'])
	package.setdefault ('build', ['%{__configure}', '%{__make}'])
	package.setdefault ('install', ['%{__makeinstall}'])

#--------------------------------------
# Package file parsing
#--------------------------------------

def parse_package (profile, package):
	load_package_defaults (profile, package)

	# walk the top level to collect and save variable tree
	vars = {}
	for k, v in package.iteritems ():
		if k in ['prep', 'build', 'install']:
			continue
		vars[k] = v

	# now process the package tree and substitute variables
	package = expand_macros (package, vars, runtime = False)

	for req in ['name', 'version', 'sources', 'prep', 'build', 'install']:
		if not req in package:
			sys.exit ('Invalid package %s: missing %s node' % (path, req))
	
	if not isinstance (package['sources'], (list, tuple)):
		sys.exit ('Invalid package %s: \'sources\' node must be a list' % path)
	elif len (package['sources']) <= 0:
		sys.exit ('Invalid package %s: no sources defined (empty list)' % path)

	return package, vars

def expand_macros (node, vars, runtime = True):
	macro_type = '%'
	if runtime:
		macro_type = '@'
	def sub_macro (m):
		macro = m.groups ()[0]
		map = macro.split (':', 2)
		if len (map) == 2 and map[0] in vars:
			if isinstance (vars[map[0]], (list, tuple)):
				map[1] = int (map[1])
				if map[1] < len (vars[map[0]]):
					return vars[map[0]][map[1]]
			elif map[1] in vars[map[0]]:
				return vars[map[0]][map[1]]
			sys.exit ('Macro \'%s\' does not contain a child \'%s\'' % (map[0], map[1]))
		if macro in vars:
			return vars[macro]
		sys.exit ('Macro \'%s\' is undefined' % macro)

	if isinstance (node, dict):
		for k, v in node.iteritems ():
			node[k] = expand_macros (v, vars, runtime)
	elif isinstance (node, (list, tuple)):
		for i, v in enumerate (node):
			node[i] = expand_macros (v, vars, runtime)
	else:
		orig_node = node
		iters = 0
		while True:
			v = re.sub ('(?<!\\\)' + macro_type + '{([\w\:]+)}', sub_macro, node)
			if v == node:
				break
			iters += 1
			if iters >= 500:
				sys.exit ('Too many macro substitutions, possible recursion: \'%s\'' % orig_node)
			node = v

	return node

#--------------------------------------
# Utility Functions
#--------------------------------------

def run_shell (cmd):
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

#--------------------------------------
# Logging
#--------------------------------------

def log (level, message):
	if level == 0:
		print '--> %s' % message
	elif level == 1:
		print '    + %s' % message
	elif level == 2:
		print '      - %s' % message

#--------------------------------------
# Main Program
#--------------------------------------

if __name__ == '__main__':
	parser = OptionParser (usage = 'usage: %prog [options] profile-path [package_names...]')
	parser.add_option ('-v', '--verbose',
		action = 'store_true', dest = 'verbose', default = False,
		help = 'show all build output (e.g. configure, make)')
	options, args = parser.parse_args ()
	
	if args == []:
		parser.print_help ()
		sys.exit (1)

	profile_path = args[0]
	packages_to_build = args[1:]

	if not os.path.exists (profile_path):
		sys.exit ('Profile %s does not exist.' % profile_path)

	try:
		exec open (profile_path).read ()
	except Exception as e:
		sys.exit ('Cannot load profile %s: %s' % (profile_path, e))

	profile_vars = {}
	for d in [profile, profile['environ']]:
		for k, v in d.iteritems ():
			profile_vars[k] = v

	profile = expand_macros (profile, profile_vars, False)
	profile.setdefault ('cpu_count', get_cpu_count ())
	profile.setdefault ('host', get_host ())
	profile.setdefault ('verbose', options.verbose)

	log (0, 'Loaded profile \'%s\' (%s)' % (profile['name'], profile['host']))

	if 'environ' in profile:
		log (0, 'Setting environment variables')
		for k, v in profile['environ'].iteritems ():
			os.environ[k] = v
			log (1, '%s = %s' % (k, os.getenv (k)))

	pwd = os.getcwd ()
	for path in profile['packages']:
		os.chdir (pwd)
		path = os.path.join (os.path.dirname (profile_path), path)
		exec open (path).read ()
		if not packages_to_build == [] and package['name'] not in packages_to_build:
			continue
		package['_path'] = path
		build_package (profile, parse_package (profile, package))
	
	print
	print 'Done.'
