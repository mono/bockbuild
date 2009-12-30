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
using System.Diagnostics;
using System.Collections.Generic;

public class NativeLibraryItem : Item
{
    public override IEnumerable<Item> Load ()
    {
        if (!IsValidConfinementItem (this)) {
            yield break;
        }

        foreach (var item in LddFile ()) {
            yield return item;
        }
    }

    private Process CreateProcess (string cmd, string args)
    {
        return Process.Start (new ProcessStartInfo (cmd, args) {
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false
        });
    }

    private IEnumerable<Item> LddFile ()
    {
        Process proc = null;

        try {
            proc = CreateProcess ("ldd", File.FullName);
        } catch {
            proc = CreateProcess ("otool", "-L " + File.FullName);
        }

        proc.WaitForExit ();
        if (proc.ExitCode != 0) {
            yield break;
        }

        yield return this;

        string line;
        while ((line = proc.StandardOutput.ReadLine ()) != null) {
            line = line.Trim ();

            int addr = line.IndexOf ('(');
            if (addr < 0) {
                continue;
            }

            line = line.Substring (0, addr);
            int map = line.IndexOf (" => ");
            if (map > 0) {
                line = line.Substring (map + 4);
            }

            var item = new NativeLibraryItem () {
                File = new FileInfo (line.Trim ()),
                Confinement = Confinement
            };

            foreach (var child_item in item.Load ()) {
                yield return child_item;
            }
        }
    }
}
