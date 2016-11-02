import fileinput

class NuGet3 (Package):
	def __init__ (self):
		Package.__init__ (self, name ='NuGet 3', version = '3.5.0',
			sources = ['https://dist.nuget.org/win-x86-commandline/v%{version}/NuGet.exe'])

	def build (self):
		pass

	def install (self):
		source = os.path.join (self.workspace, 'NuGet.exe')
		target = os.path.join (self.staged_prefix, 'lib/mono/nuget/NuGet3.exe')
		ensure_dir (os.path.dirname (target))
		shutil.move (source, target)

		launcher = os.path.join (self.staged_prefix, "bin/nuget3")
		ensure_dir (os.path.dirname (launcher))
		with open(launcher, "w") as output:
			output.write ("#!/bin/sh\n")
			output.write ('exec "{0}/bin/mono" $MONO_OPTIONS "{1}" "$@"\n'.format (self.staged_prefix, target))
		os.chmod (launcher, 0755)
NuGet3 ()