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
using System.Diagnostics;
using System.Collections.Generic;
using System.Text.RegularExpressions;

public class Solitary
{
    public List<Regex> PathBlacklist { get; private set; }
    public List<Item> Items { get; private set; }
    public List<string> SearchPaths { get; private set; }
    public Dictionary<string, int> EscapedItems { get; set; }
    public string MonoPrefix { get; set; }
    public string ConfinementRoot { get; set; }
    public string OutputPath { get; set; }

    private class BlacklistComparer : IEqualityComparer<string>
    {
        public bool Equals (string a, string b) { return Path.GetFileName (b).StartsWith (a); }
        public int GetHashCode (string o) { return o.GetHashCode (); }
    }

    public Solitary ()
    {
        PathBlacklist = new List<Regex> ();
        Items = new List<Item> ();
        SearchPaths = new List<string> ();
        EscapedItems = new Dictionary<string, int> ();

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

    public void LoadPathBlacklist (string blacklistFile)
    {
        if (blacklistFile == null) {
            return;
        }

        using (var reader = new StreamReader (blacklistFile)) {
            string line = null;
            while ((line = reader.ReadLine ()) != null) {
                line = line.Trim ();
                if (!String.IsNullOrEmpty (line) && line[0] != '#') {
                    PathBlacklist.Add (new Regex (line, RegexOptions.Compiled));
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

    public void CreateBundle (bool strip)
    {
        Directory.CreateDirectory (OutputPath);

        foreach (var item in Items) {
            try {
                item.Relocate ();
            } catch {
            }
            /*var native_item = item as NativeLibraryItem;
            if (strip && native_item != null) {
                native_item.Strip ();
            }*/
        }

        int count = 0;
        foreach (var item in Items) {
            var native_item = item as NativeLibraryItem;
            if (native_item != null) {
                count++;
                native_item.RelocateDependencies ();
            }
        }

        Console.WriteLine ("{0} native libraries processed.", count);
    }
}
