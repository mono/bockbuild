// 
// AssemblyItem.cs
//  
// Author:
//   Aaron Bockover <abockover@novell.com>
// 
// Copyright 2009-2010 Novell, Inc.
// 
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

using System;
using System.IO;
using System.Collections.Generic;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Xml.XPath;

public class AssemblyItem : Item
{
    public Assembly Assembly { get; private set; }

    public AssemblyItem (Solitary confinement, FileInfo file) : base (confinement, file)
    {
        var tempFile = FindPossibleTempFile ();
        if (tempFile == null) {
            // could be a referenced assembly, such as mscorlib
            tempFile = file.FullName;
        }
        Assembly = Assembly.LoadFrom (tempFile);
    }

    public AssemblyItem (Solitary confinement, Assembly assembly) : base (confinement, new FileInfo (assembly.Location))
    {
        if (assembly == null) {
            throw new ArgumentNullException ("assembly");
        }

        Assembly = assembly;
    }

    private string FindPossibleTempFile ()
    {
        if (String.IsNullOrEmpty (Confinement.TempPath)) {
            throw new InvalidOperationException ("Confinement.TempPath cannot be empty.");
        }
        if (!Directory.Exists (Confinement.TempPath)) {
            throw new InvalidOperationException ("Confinement.TempPath should have been created at this point.");
        }
        var tempPathElements = new DirectoryInfo (Confinement.TempPath).GetFileSystemInfos ();
        var assemblyFileName = System.IO.Path.GetFileName (File.FullName);
        foreach (var fileSystemInfo in tempPathElements) {
            if (Directory.Exists (fileSystemInfo.FullName)) {
                throw new InvalidOperationException ("There cannot be subfolders inside Confinement.TempPath.");
            }
            if (System.IO.Path.GetFileName (fileSystemInfo.FullName).Equals (assemblyFileName)) {
                return fileSystemInfo.FullName;
            }
        }
        return null;
    }

    public override IEnumerable<Item> Load ()
    {
        if (!IsValidConfinementItem (this)) {
            yield break;
        }

        yield return this;
        
        var sibling = Item.Resolve (Confinement, File.FullName + ".mdb");
        if (sibling != null) {
            yield return sibling;
        } 

        sibling = Item.Resolve (Confinement, File.FullName + ".config");
        if (sibling != null) {
            yield return sibling;
        }

        foreach (var item in ReadAssembly ()) {
            yield return item;
        }

        foreach (var rname in Assembly.GetReferencedAssemblies ()) {
            var loadedReference = Assembly.Load (rname.FullName);
            var ritem = new AssemblyItem (Confinement, loadedReference);
            foreach (var item in ritem.Load ()) {
                yield return item;
            }
        }
    }

    private IEnumerable<Item> ReadAssembly ()
    {
        var binding_flags = 
            BindingFlags.NonPublic | 
            BindingFlags.Public | 
            BindingFlags.Instance | 
            BindingFlags.Static;

        var pinvoke_modules = new List<string> ();

        foreach (var type in Assembly.GetTypes ()) {
            foreach (var method in type.GetMethods (binding_flags)) {
                if ((method.Attributes & MethodAttributes.PinvokeImpl) != 0) {
                    foreach (var attr in method.GetCustomAttributes (typeof (DllImportAttribute), true)) {
                        string module = ((DllImportAttribute)attr).Value;
                        if (!pinvoke_modules.Contains (module)) {
                            pinvoke_modules.Add (module);
                        }
                    }
                }
            }
        }

        foreach (var module in pinvoke_modules) {
            var lib = LocateNativeLibrary (Assembly.Location, module);
            if (lib != null) {
                var item = Item.Resolve (Confinement, new FileInfo (lib));
                if (item == null) {
                    continue;
                }
                foreach (var child_item in item.Load ()) {
                    yield return child_item;
                }
            }
        }
    }
 
    private string LocateNativeLibrary (string assemblyPath, string pinvokeModule)
    {
        var asm_config = assemblyPath + ".config"; 
        var module = pinvokeModule;

        if (System.IO.File.Exists (asm_config)) {
            module = FindNativeLibraryForDllMap (asm_config, pinvokeModule);
        }
        
        if (Confinement.MonoPrefix != null) {
            var mono_config_path = Path.Combine (Confinement.MonoPrefix, "etc/mono/config");
            if (module == pinvokeModule && System.IO.File.Exists (mono_config_path)) {
                module = FindNativeLibraryForDllMap (mono_config_path, pinvokeModule);
            }
        }

        pinvokeModule = module;

        foreach (var path in Confinement.SearchPaths) {
            var names = new string [] {
                pinvokeModule,
                pinvokeModule + ".so",
                pinvokeModule + ".dylib",
                "lib" + pinvokeModule,
                "lib" + pinvokeModule + ".so",
                "lib" + pinvokeModule + ".dylib"
            };

            foreach (var name in names) {
                var full_name = Path.Combine (path, name);
                if (System.IO.File.Exists (full_name)) {
                    return full_name;
                }
            }
        }

        return null;
    }

    private static string FindNativeLibraryForDllMap (string asmConfig, string pinvokeModule)
    {
        var navigator = new XPathDocument (asmConfig).CreateNavigator ();
        var expression = navigator.Compile ("/configuration/dllmap");
        var iter = navigator.Select (expression);
            
        while (iter.MoveNext ()) {
            if (iter.Current.GetAttribute ("dll", navigator.NamespaceURI) != pinvokeModule) {
                continue;
            }

            // FIXME: make this configurable on the confinement
            var os = iter.Current.GetAttribute ("os", navigator.NamespaceURI); 
            if (String.IsNullOrEmpty (os) || os == "osx" || os == "!windows") {
                return iter.Current.GetAttribute ("target", navigator.NamespaceURI);
            }
        }

        return pinvokeModule;
    }
}


