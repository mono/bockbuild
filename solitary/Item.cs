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
    ELF,
    Data
}

public abstract class Item
{
    public Solitary Confinement { get; private set; }
    public abstract IEnumerable<Item> Load ();

    public FileInfo OriginalFile { get; private set; }

    private FileInfo file;
    public FileInfo File {
        get { return file; }
        protected set {
            if (value == null) {
                file = null;
                return;
            }

            file = value;
            if (OriginalFile == null) {
                OriginalFile = file;
            }
        }
    }

    protected Item (Solitary confinement)
    {
        Confinement = confinement;
    }

    public bool IsValidConfinementItem (Item item)
    {
        return IsValidConfinementItem (item, true);
    }
    
    public bool IsValidConfinementItem (Item item, bool checkExists)
    {
        if (!String.IsNullOrEmpty (ProcessTools.RealConfinementRoot) &&
            item.File.FullName.StartsWith (ProcessTools.RealConfinementRoot)) {
            string path = item.File.FullName.Replace (ProcessTools.RealConfinementRoot, Confinement.ConfinementRoot);
            item.File = new FileInfo (path);
        }

        if (Confinement.ConfinementRoot != null &&
            !item.File.FullName.StartsWith (Confinement.ConfinementRoot)) {
            if (Confinement.EscapedItems.ContainsKey (item.File.FullName)) {
                Confinement.EscapedItems[item.File.FullName]++;
            } else {
                Confinement.EscapedItems[item.File.FullName] = 1;
            }
            return false;
        } else if (!checkExists) {
            return true;
        }

        return !Confinement.Items.Exists (c => c.File.FullName == item.File.FullName);
    }

    public string GetRelocationPath ()
    {
        return GetRelocationPath (File.FullName);
    }

    public string GetRelocationPath (string path)
    {
        if (Confinement.ConfinementRoot != null) {
            path = path.Substring (Confinement.ConfinementRoot.Length + 1);
        }
        return Path.Combine (Confinement.OutputPath, path);
    }

    public virtual void Relocate ()
    {
        var path = GetRelocationPath ();
        Directory.CreateDirectory (Path.GetDirectoryName (path));
        System.IO.File.Copy (File.FullName, path);
        File = new FileInfo (path);
    }

    public static Item Resolve (Solitary confinement, string path)
    {
        return Resolve (confinement, new FileInfo (path));
    }

    public static Item Resolve (Solitary confinement, FileInfo file)
    {
        if (!file.Exists || file.Name.StartsWith (".")) {
            return null;
        }

        Item item = null;

        foreach (var regex in confinement.PathBlacklist) {
            if (regex.IsMatch (file.FullName)) {
                return null;
            }
        }

        if (!String.IsNullOrEmpty (ProcessTools.RealConfinementRoot) &&
            file.FullName.StartsWith (ProcessTools.RealConfinementRoot)) {
            string path = file.FullName.Replace (ProcessTools.RealConfinementRoot, confinement.ConfinementRoot);
            file = new FileInfo (path);
        }

        if (SymlinkItem.IsSymlink (file.FullName)) {
            return new SymlinkItem (confinement) {
                File = file
            };
        }

        switch (GetFileType (file)) {
            case FileType.PE32Executable: 
                item = new AssemblyItem (confinement);
                break;
            case FileType.MachO:
            case FileType.ELF:
                item = new NativeLibraryItem (confinement);
                break;
            default:
                item = new DataItem (confinement);
                break;
        }

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
        
        proc.Dispose ();
        
        if (line == null) {
            return FileType.Data;
        }

        if (line.Contains ("Mach-O")) {
            return FileType.MachO;
        } else if (line.Contains ("PE32 executable")) {
            return FileType.PE32Executable;
        } else if (line.Contains ("ELF")) {
            return FileType.ELF;
        }

        return FileType.Data;
    }
}

