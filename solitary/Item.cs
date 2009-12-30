// 
// Item.cs
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

using Mono.Unix;

public enum FileType
{
    PE32Executable,
    MachO,
    Data
}

public abstract class Item
{
    public Solitary Confinement { get; set; }
    public abstract IEnumerable<Item> Load ();

    private FileInfo file;
    public FileInfo File {
        get { return file; }
        set {
            if (value == null) {
                file = null;
                return;
            }

            file = value;
            var link = new UnixSymbolicLinkInfo (file.FullName);
            if (link.HasContents) {
                file = new FileInfo (link.GetContents ().FullName);
            }
        }
    }

    public bool IsValidConfinementItem (Item item)
    {
        if (Confinement.ConfinementRoot != null &&
            !item.File.FullName.StartsWith (Confinement.ConfinementRoot)) {
            return false;
        }

        return !Confinement.Items.Exists (c => c.File.FullName == item.File.FullName);
    }

    public static Item Resolve (Solitary confinement, FileInfo file)
    {
        if (file.Name.StartsWith (".")) {
            return null;
        }

        Item item = null;

        foreach (var regex in confinement.PathBlacklist) {
            if (regex.IsMatch (file.FullName)) {
                return null;
            }
        }

        switch (GetFileType (file)) {
            case FileType.PE32Executable: 
                item = new AssemblyItem ();
                break;
            case FileType.MachO:
                item = new NativeLibraryItem ();
                break;
            default:
                item = new DataItem ();
                break;
        }

        item.Confinement = confinement;
        item.File = file;
        return item;
    }

    public static FileType GetFileType (FileInfo file)
    {
        var proc = ProcessTools.CreateProcess ("file", file.FullName);
        if (proc == null) {
            return FileType.Data;
        }
        
        var line = proc.StandardOutput.ReadLine ();
        if (line == null) {
            return FileType.Data;
        }

        if (line.Contains ("Mach-O")) {
            return FileType.MachO;
        } else if (line.Contains ("PE32 executable")) {
            return FileType.PE32Executable;
        }

        return FileType.Data;
    }
}

