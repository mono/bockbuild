#!/usr/bin/env python

import os
import sys
import re
import glob
import shutil
import urllib
import subprocess

def build_package (package, vars):
	package_dir = os.path.dirname (package['_path'])
	package_build_dir = os.path.join (config['build_root'],
		'%s-%s' % (package['name'], package['version']))
	build_success_file = os.path.join (config['build_root'],
		'%s-%s.success' % (package['name'], package['version']))

	if os.path.exists (build_success_file):
		print 'Skipping %s - already built' % package['name']
		return

	print 'Building %s on %s (%s CPU)' % (package['name'], get_host (), get_cpu_count ())

	# Set up the directories
	if not os.path.exists (config['build_root']) or not os.path.isdir (config['build_root']):
		os.makedirs (config['build_root'], 0755)

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
				run_shell (step)

	open (build_success_file, 'w').close ()

def load_package_defaults (config, package):
	# path macros
	package['_build_root'] = os.path.join (config['build_root'], '_install')
	package['_prefix'] = package['_build_root']

	# tool macros
	package['__configure'] = './configure --prefix=%{_prefix}'
	package['__make'] = 'make -j%s' % get_cpu_count ()
	package['__makeinstall'] = '%{__make} install'

	# install default sections if they are missing
	if not 'prep' in package:
		package['prep'] = ['tar xf @{sources:0}', 'cd %{name}-%{version}']
	if not 'build' in package:
		package['build'] = ['%{__configure}', '%{__make}']
	if not 'install' in package:
		package['install'] = ['%{__makeinstall}']

#--------------------------------------
# Package file parsing
#--------------------------------------

def parse_package (package):
	load_package_defaults (config, package)

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

__packages = []
config = {
	'build_root': os.path.join (os.getcwd (), 'build-root')
}

def load_file (path):
	package = None
	packages = None
	build_env = None
	if not os.path.isfile (path):
		sys.exit ('Error: %s is not a file' % path)
	exec open (path).read ()
	if isinstance (package, dict):
		package['_path'] = path
		__packages.append (parse_package (package))
	elif isinstance (packages, (list, tuple)):
		pass
		for package in packages:
			load_file (package)
	if isinstance (build_env, dict):
		print '%s is overriding build_env config' % path
		globals ()['config'] = build_env 

if __name__ == '__main__':
	for arg in sys.argv[1:]:
		load_file (arg)
	
	config_vars = {}
	for d in [config, config['environ']]:
		for k, v in d.iteritems ():
			config_vars[k] = v
	config = expand_macros (config, config_vars, False)

	if config['environ']:
		log (0, 'Setting environment variables')
		for k, v in config['environ'].iteritems ():
			os.environ[k] = v
			log (1, '%s = %s' % (k, os.getenv (k)))

	for package, vars in __packages:
		build_package (package, vars)
