// 
// Solitary.cs
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

public class Solitary
{
    public List<string> Blacklist { get; private set; }
    public List<Item> Items { get; private set; }
    public List<string> SearchPaths { get; private set; }
    public string MonoPrefix { get; set; }
    public string ConfinementRoot { get; set; }

    private class BlacklistComparer : IEqualityComparer<string>
    {
        public bool Equals (string a, string b) { return Path.GetFileName (b).StartsWith (a); }
        public int GetHashCode (string o) { return o.GetHashCode (); }
    }

    public Solitary ()
    {
        Blacklist = new List<string> ();
        Items = new List<Item> ();
        SearchPaths = new List<string> ();

        FindNativeLibrarySearchPaths ();
    }

    private void FindNativeLibrarySearchPaths ()
    {
        foreach (var var in new [] { "LD_LIBRARY_PATH", "DYLD_LIBRARY_PATH", "DYLD_FALLBACK_LIBRARY_PATH" }) {
            var value = Environment.GetEnvironmentVariable (var);
            if (!String.IsNullOrEmpty (value)) {
                foreach (var path in value.Split (':')) {
                    SearchPaths.Add (path);
                }
            }
        }

        FindNativeLibrarySearchPaths ("/etc/ld.so.conf");
    }

    private void FindNativeLibrarySearchPaths (string ldConfigPath)
    {
        string line;

        if (!File.Exists (ldConfigPath)) {
            return;
        }

        using (var reader = new StreamReader (ldConfigPath)) {
            while ((line = reader.ReadLine ()) != null) {
                line = line.Trim ();
                if (line.StartsWith ("include ")) {
                    var expr = line.Substring (8);
                    var dir = Path.GetDirectoryName (expr);
                    expr = expr.Substring (expr.LastIndexOf (Path.DirectorySeparatorChar) + 1);
                    foreach (var path in Directory.GetFiles (dir, expr)) {
                        FindNativeLibrarySearchPaths (path);
                    }
                } else {
                    SearchPaths.Add (line);
                }
            }
        }
    }

    public void LoadBlacklist (string blacklistFile)
    {
        if (blacklistFile == null) {
            return;
        }

        using (var reader = new StreamReader (blacklistFile)) {
            string line = null;
            while ((line = reader.ReadLine ()) != null) {
                line = line.Trim ();
                if (!String.IsNullOrEmpty (line) && line[0] != '#') {
                    Blacklist.Add (line);
                }
            }
        }
    }
    
    public IEnumerable<Item> Walk (string path)
    {
        return Walk (Directory.Exists (path)
            ? (FileSystemInfo)new DirectoryInfo (path)
            : (FileSystemInfo)new FileInfo (path));
    }

    public IEnumerable<Item> Walk (FileSystemInfo fsi)
    {
        var hidden = fsi.Name.StartsWith (".");
        var dir = fsi as DirectoryInfo;
        var file = fsi as FileInfo;

        if (hidden) {
            yield break;
        } else if (dir != null) {
            foreach (var child_dir in dir.GetFileSystemInfos ()) {
                foreach (var item in Walk (child_dir)) {
                    yield return item;
                }
            }
        } else if (file != null) {
            var item = Item.Resolve (this, file);
            if (item != null) {
                yield return item;
            }
        }
    } 
}
