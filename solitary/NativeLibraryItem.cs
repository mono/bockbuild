// 
// NativeLibraryItem.cs
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

public class NativeLibraryItem : Item
{
    public NativeLibraryItem (Solitary confinement) : base (confinement)
    {
    }

    public override IEnumerable<Item> Load ()
    {
        if (!IsValidConfinementItem (this)) {
            yield break;
        }

        var deps = ProcessTools.GetNativeDependencies (File);
        if (deps == null) {
            yield break;
        }

        yield return this;
        
        foreach (var dep in deps) {
            var item = Item.Resolve (Confinement, new FileInfo (dep));
            if (item == null) {
                continue;
            }
            
            foreach (var child_item in item.Load ()) {
                yield return child_item;
            }
        }
    }

    public void Strip ()
    {
        var proc = ProcessTools.CreateProcess ("strip",
            String.Format ("-u -r \"{0}\"", File.FullName));
        if (proc != null) {
            proc.Dispose ();
        }
    }

    public void RelocateDependencies ()
    {
        if (ProcessTools.Host != ProcessHost.Darwin) {
            if (String.IsNullOrEmpty (ProcessTools.RealConfinementRoot)) {
                throw new ApplicationException ("Relocation not supported on anything but Darwin");
            } else {
                return;
            }
        }

        var proc = ProcessTools.CreateProcess ("otool", "-D " + File.FullName);
        if (proc == null) {
            return;
        }
        
        string t, dep_id = null;
        while ((t = proc.StandardOutput.ReadLine ()) != null) {
            dep_id = t.Trim ();
            if (dep_id.StartsWith (Confinement.ConfinementRoot)) {
                dep_id = dep_id.Substring (Confinement.ConfinementRoot.Length + 1); 
            }

            dep_id = Path.GetFileName (t.Trim ());
        }
            // dep_id = PathExtensions.RelativePath (File.FullName,
            //    Path.GetDirectoryName (dep_id.Trim ()));

        proc.Dispose ();

        int reloc_count = 0;

        var deps = ProcessTools.GetNativeDependencies (File);
        foreach (var dep in deps) {
            if (Confinement.ConfinementRoot != null &&
                !dep.StartsWith (Confinement.ConfinementRoot)) {
                continue;
            }
            
            // var rel_dep = PathExtensions.RelativePath (dep,
            //    Path.GetDirectoryName (OriginalFile.FullName));
            
            var rel_dep = dep.Substring (Confinement.ConfinementRoot.Length + 1);
            rel_dep = Path.GetFileName (rel_dep);
            proc = ProcessTools.CreateProcess ("install_name_tool", String.Format (
                "-change \"{0}\" \"{1}\" -id \"{2}\" \"{3}\"",
                dep, rel_dep, dep_id, File.FullName));
            if (proc != null) {
                reloc_count++;
                proc.Dispose ();
            }
        }

        Console.WriteLine (" + {0} ({1} relocs)", File.Name, reloc_count);
    }
}
