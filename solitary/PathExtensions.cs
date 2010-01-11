// 
// PathExtensions.cs
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

public static class PathExtensions
{
    public static string RelativePath (string path, string start)
    {
        var start_list = Path.GetFullPath (start).Split (Path.DirectorySeparatorChar);
        var path_list = Path.GetFullPath (path).Split (Path.DirectorySeparatorChar);
        var shared_count = CommonPrefix (path_list, start_list).Length;

        var rel_list = new List<string> ();
        for (int i = 0; i < start_list.Length - shared_count; rel_list.Add (".."), i++);
        for (int i = shared_count; i < path_list.Length; rel_list.Add (path_list[i++]));
        
        return String.Join (Path.DirectorySeparatorChar.ToString (), rel_list.ToArray ());
    }

    public static string [] CommonPrefix (string [] a, string [] b)
    {
        var min = Math.Min (a.Length, b.Length);
        var common = new List<string> (min);
        for (int i = 0; i < min && a[i] == b[i]; common.Add (a[i++]));
        return common.ToArray ();
    }
}
