// 
// ProcessTools.cs
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

public enum ProcessHost
{
    Linux,
    Darwin,
    Windows
}

public static class ProcessTools
{
    public static ProcessHost Host { get; private set; }

    static ProcessTools ()
    {
        var uname = CreateProcess ("uname");
        if (uname == null) {
            Host = ProcessHost.Windows;
            return;
        }
        
        switch (uname.StandardOutput.ReadToEnd ().Trim ().ToLower ()) {
            case "darwin": Host = ProcessHost.Darwin; break;
            case "linux": Host = ProcessHost.Linux; break;
        }
    }

    public static Process CreateProcess (string cmd)
    {
        return CreateProcess (cmd, null);
    }

    public static Process CreateProcess (string cmd, string args)
    {
        try {
            var proc = Process.Start (new ProcessStartInfo (cmd, args) {
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false
            });

            proc.WaitForExit ();
            if (proc.ExitCode != 0) {
                return null;
            }
            
            return proc;
        } catch {
            return null;
        }
    }
 
    public static List<string> GetNativeDependencies (FileInfo file)
    {
        var proc = Host == ProcessHost.Darwin
            ? CreateProcess ("otool", "-L " + file.FullName)
            : CreateProcess ("ldd", file.FullName);
        
        if (proc == null) {
            return null;
        }

        var items = new List<string> ();
        string line;

        while ((line = proc.StandardOutput.ReadLine ()) != null) {
            var match = Regex.Match (line, @"^\s+(.+)\(.+");
            if (match.Success) {
                items.Add (match.Groups[1].Value.Trim ());
            }
        }

        return items;
    }
}
