import os
import string

class IronLanguagesPackage(GitHubTarballPackage):

	def __init__(self):
		GitHubTarballPackage.__init__(self,
			'IronLanguages', 'iron-languages',
			'2.11',
			'de63773744ccf9873c1826470730ae0446fd64d7',
			configure = '')

		#override: avoid naming the package 'main' because of the repo name
		self.sources = ['https://github.com/%{organization}/main/tarball/%{revision}']
		self.source_dir_name = '%s-%s-%s' % ( self.organization, 'main', self.revision[:7] )

	def build (self):
		self.ironruby = os.path.join (os.getcwd(), 'ironruby', 'bin') + os.sep
		self.ironpython = os.path.join (os.getcwd(), 'ironpython', 'bin') + os.sep
		self.sh ('xbuild /p:Configuration=Release /p:OutDir="%{ironruby}" Solutions/Ruby.sln')
		self.sh ('xbuild /p:Configuration=Release /p:OutDir="%{ironpython}" Solutions/IronPython.Mono.sln')


	def install_wrapper_scripts (self, path, ironpython_or_ironruby):
		for cmd, ext in map(os.path.splitext, os.listdir (path)):
			if ext != '.exe': continue
			wrapper = os.path.join (self.staged_prefix, "bin", cmd)
			with open(wrapper, "w") as output:
				output.write ("#!/bin/sh\n")
				output.write ("exec {0}/bin/mono {0}/lib/{1}/{2}.exe \"$@\"\n".format (self.staged_prefix, ironpython_or_ironruby, cmd))
			os.chmod (wrapper, 0755)

	def install (self):
		self.ironruby = os.path.join (os.getcwd(), 'ironruby', 'bin') + os.sep
		self.ironpython = os.path.join (os.getcwd(), 'ironpython', 'bin') + os.sep

		self.sh ("mkdir -p %{staged_prefix}/lib/ironruby/")
		self.sh ("cp -R %{ironruby} %{staged_prefix}/lib/ironruby/")
		self.install_wrapper_scripts (self.ironruby, 'ironruby')

		self.sh ("mkdir -p %{staged_prefix}/lib/ironpython/")
		self.sh ("cp -R %{ironpython} %{staged_prefix}/lib/ironpython/")
		self.install_wrapper_scripts (self.ironpython, 'ironpython')

IronLanguagesPackage()
