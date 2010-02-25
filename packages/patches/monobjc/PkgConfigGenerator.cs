using System;
using System.Reflection;
using System.Collections.Generic;

public static class PkgConfigGenerator
{
    private static List<Assembly> assemblies = new List<Assembly> ();

    public static void Main (string [] args)
    {
        var asm = Assembly.LoadFrom (args[0]);
        var asm_name = asm.GetName ();
        WalkAssembly (asm);

        Console.WriteLine ("Name: {0}", asm_name.Name);
        Console.WriteLine ("Description:");
        Console.WriteLine ("Version: {0}", asm_name.Version);
        Console.Write ("Libs: ");
        foreach (var dep in assemblies) {
            if (dep.GetName ().Name != "mscorlib") {
                Console.Write ("-r:{0} ", dep.Location);
            }
        }
        Console.WriteLine ();
    }

    private static void WalkAssembly (Assembly asm)
    {
        if (assemblies.Contains (asm)) {
            return;
        }

        assemblies.Add (asm);

        foreach (var rname in asm.GetReferencedAssemblies ()) {
            WalkAssembly (Assembly.Load (rname.FullName));
        }
    }
}
