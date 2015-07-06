// 
// SymlinkItem.cs
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

public class SymlinkItem : Item
{
    private UnixSymbolicLinkInfo link;

    public SymlinkItem (Solitary confinement) : base (confinement)
    {
    }
    
    public static bool IsSymlink (string path)
    {
        return new UnixSymbolicLinkInfo (path).HasContents;
    }

    public override IEnumerable<Item> Load ()
    {
        if (!IsValidConfinementItem (this)) {
            yield break;
        }

        link = new UnixSymbolicLinkInfo (File.FullName);
        if (!link.HasContents) {
            yield break;
        }

        yield return this;

        var item = Item.Resolve (Confinement,
            new FileInfo (link.GetContents ().FullName));

        foreach (var child_item in item.Load ()) {
            yield return child_item;
        }
    }

    public override void Relocate ()
    {
        var link_path = GetRelocationPath ();
        var link_contents_path = PathExtensions.RelativePath (
            link.GetContents ().FullName,
            Path.GetDirectoryName (File.FullName));
        Directory.CreateDirectory (Path.GetDirectoryName (link_path));
        Console.WriteLine ("Creating {0}", link_path);
        new UnixSymbolicLinkInfo (link_path).CreateSymbolicLinkTo (link_contents_path);
    }
}
