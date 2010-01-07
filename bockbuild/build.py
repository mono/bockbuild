#!/usr/bin/env python

import os
import sys
import re
import glob
import shutil
import urllib
from util import *
from optparse import OptionParser

def build_package (profile, (package, vars)):
	package_dir = os.path.dirname (package['_path'])
	package_dest_dir = os.path.join (profile.build_root,
		'%s-%s' % (package['name'], package['version']))
	package_build_dir = os.path.join (package_dest_dir, '_build')
	build_success_file = os.path.join (profile.build_root,
		'%s-%s.success' % (package['name'], package['version']))

	if os.path.exists (build_success_file):
		print 'Skipping %s - already built' % package['name']
		return

	print 'Building %s on %s (%s CPU)' % (package['name'], profile.host, profile.cpu_count)

	# Set up the directories
	if not os.path.exists (profile.build_root) or not os.path.isdir (profile.build_root):
		os.makedirs (profile.build_root, 0755)

	shutil.rmtree (package_build_dir, ignore_errors = True)
	os.makedirs (package_build_dir)

	# Copy/download sources into the build root, and adjust the
	# sources list in the package object to be relative local
	# filenames from the build root directory for later
	log (0, 'Retrieving sources')
	local_sources = []
	for source in package['sources']:
		source = legacy_expand_macros (source, vars)
		local_source = os.path.join (package_dir, source)
		local_source_file = os.path.basename (local_source)
		local_dest_file = os.path.join (package_dest_dir, local_source_file)
		local_sources.append (local_dest_file)

		if os.path.isfile (local_dest_file):
			log (1, 'using cached source: %s' % local_dest_file)
		else:
			if os.path.isfile (local_source):
				log (1, 'copying local source: %s' % local_source_file)
				shutil.copy2 (local_source, local_dest_file)
			elif source.startswith (('http', 'https', 'ftp')):
				log (1, 'downloading remote source: %s' % source)
				urllib.urlretrieve (source, local_dest_file)

	package['sources'] = local_sources
	
	os.chdir (package_build_dir)

	for phase in profile.run_phases:
		log (0, '%sing %s' % (phase.capitalize (), package['name']))
		for step in package[phase]:
			if hasattr (step, '__call__'):
				log (1, '<py call: %s>' % step.__name__)
				step (package)
				continue
			step = legacy_expand_macros (step, package)
			log (1, step)
			if step.startswith ('cd '):
				os.chdir (step[3:])
			else:
				if not profile.verbose:
					step = '( %s ) &>/dev/null' % step
				run_shell (step)

	open (build_success_file, 'w').close ()

def load_package_defaults (profile, package):
	# path macros
	package['_build_root'] = os.path.join (profile.build_root, '_install')
	package['_prefix'] = package['_build_root']

	# tool macros
	package['__configure'] = './configure --prefix=%{_prefix}'
	package['__make'] = 'make -j%s' % profile.cpu_count
	package['__makeinstall'] = 'make install'

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
	package = legacy_expand_macros (package, vars, runtime = False)

	for req in ['name', 'version', 'sources', 'prep', 'build', 'install']:
		if not req in package:
			sys.exit ('Invalid package %s: missing %s node' % (path, req))
	
	if not isinstance (package['sources'], (list, tuple)):
		sys.exit ('Invalid package %s: \'sources\' node must be a list' % path)

	return package, vars

def legacy_expand_macros (node, vars, runtime = True):
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
			node[k] = legacy_expand_macros (v, vars, runtime)
	elif isinstance (node, (list, tuple)):
		for i, v in enumerate (node):
			node[i] = legacy_expand_macros (v, vars, runtime)
	elif isinstance (node, str):
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
# Logging
#--------------------------------------

def log (level, message):
	if level == 0:
		print '==> %s' % message
	elif level == 1:
		print '    + %s' % message
	elif level == 2:
		print '      - %s' % message

#--------------------------------------
# Main Program
#--------------------------------------

def main (profile):
	default_run_phases = ['prep', 'build', 'install']

	parser = OptionParser (usage = 'usage: %prog [options] [package_names...]')
	parser.add_option ('-b', '--build',
		action = 'store_true', dest = 'do_build', default = False,
		help = 'build the profile')
	parser.add_option ('-v', '--verbose',
		action = 'store_true', dest = 'verbose', default = False,
		help = 'show all build output (e.g. configure, make)')
	parser.add_option ('-i', '--include-phase',
		action = 'append', dest = 'include_run_phases', default = [],
		help = 'explicitly include a build phase to run %s' % default_run_phases)
	parser.add_option ('-x', '--exclude-phase',
		action = 'append', dest = 'exclude_run_phases', default = [],
		help = 'explicitly exclude a build phase from running %s' % default_run_phases)
	parser.add_option ('-s', '--only-sources',
		action = 'store_true', dest = 'only_sources', default = False,
		help = 'only fetch sources, do not run any build phases')
	parser.add_option ('-e', '--environment', default = False,
		action = 'store_true', dest = 'dump_environment',
		help = 'Dump the profile environment as a shell-sourceable list of exports ')
	options, args = parser.parse_args ()
	
	packages_to_build = args
	profile.verbose = options.verbose
	profile.run_phases = default_run_phases

	if options.dump_environment:
		profile.env.compile ()
		profile.env.dump ()
		sys.exit (0)

	if not options.do_build:
		parser.print_help ()
		sys.exit (1)

	if not options.include_run_phases == []:
		profile.run_phases = options.include_run_phases
	for exclude_phase in options.exclude_run_phases:
		profile.run_phases.remove (exclude_phase)
	if options.only_sources:
		profile.run_phases = []

	for phase_set in [profile.run_phases,
		options.include_run_phases, options.exclude_run_phases]:
		for phase in phase_set:
			if phase not in default_run_phases:
				sys.exit ('Invalid run phase \'%s\'' % phase)

	log (0, 'Loaded profile \'%s\' (%s)' % (profile.name, profile.host))
	for phase in profile.run_phases:
		log (1, 'Phase \'%s\' will run' % phase)

	profile.env.compile ()
	profile.env.export ()
	log (0, 'Setting environment variables')
	for k in profile.env.get_names ():
		log (1, '%s = %s' % (k, os.getenv (k)))

	pwd = os.getcwd ()
	for path in profile.packages:
		os.chdir (pwd)
		path = os.path.join (os.path.dirname (sys.argv[0]), path)
		exec compile (open (path).read (), path, 'exec')
		if not packages_to_build == [] and package['name'] not in packages_to_build:
			continue
		package['_path'] = path
		build_package (profile, parse_package (profile, package))
	
	print
	print 'Done.'
