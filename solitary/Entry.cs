// 
// Entry.cs
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
using System.Collections.Generic;

using Mono.Options;

public static class Entry
{
    public static void Main (string [] args)
    {
        var solitary = new Solitary ();

        bool show_help = false;
        string blacklist_file = null;
        List<string> paths = null;

        var p = new OptionSet () {
            { "p|mono-prefix=", "set the mono prefix (e.g. to find etc/mono/config)", v => solitary.MonoPrefix = v },
            { "r|root=", "set the confinement root - any files outside of the root will be ignored", v => solitary.ConfinementRoot = v },
            { "b|blacklist=", "blacklist file to exclude native libraries from the summary", v => blacklist_file = v },
            { "h|help", "show this message and exit", v => show_help = v != null }
        };

        try {
            paths = p.Parse (args);
        } catch (OptionException e) {
            Console.Write ("Solitary: ");
            Console.WriteLine (e.Message);
            Console.WriteLine ("Try --help for more information");
            return;
        }

        if (show_help) {
            Console.WriteLine ("Usage: Shoes [OPTIONS]+ <managed_dir1> <managed_dir2>...");
            Console.WriteLine ();
            Console.WriteLine ("Options:");
            p.WriteOptionDescriptions (Console.Out);
            return;
        }
        
        solitary.LoadBlacklist (blacklist_file);
        
        long total_size = 0;
        foreach (var path in paths) {
            foreach (var item in solitary.Walk (path)) {
                foreach (var collect_item in item.Load ()) {
                    solitary.Items.Add (collect_item);
                    total_size += collect_item.File.Length;

                    if (solitary.ConfinementRoot != null) {
                        Console.WriteLine (collect_item.File.FullName.Substring (solitary.ConfinementRoot.Length + 1));
                    } else {
                        Console.WriteLine (collect_item.File.FullName);
                    }
                }
            }
        }
        Console.WriteLine (total_size);
    }
}
