using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection.Metadata;
using System.Text;
using System.Threading.Tasks;

namespace WindowsApp
{
    internal static class Constants
    {
        public static string pythonScriptsPath()
        {
            string path = AppDomain.CurrentDomain.BaseDirectory;
            path = path.Remove(path.LastIndexOfAny(new char[] { '\\' }, path.LastIndexOf('\\') - 1));
            path = String.Join(@"\", path.Split('\\').Reverse().Skip(2).Reverse());
            return path + "\\ExecutablesScripts\\dist\\";
        } 

        public static string savedDataPath()
        {
            string path = AppDomain.CurrentDomain.BaseDirectory;
            path = path.Remove(path.LastIndexOfAny(new char[] { '\\' }, path.LastIndexOf('\\') - 1));
            path = String.Join(@"\", path.Split('\\').Reverse().Skip(2).Reverse());
            return path + "\\stocksData\\lists\\";
        }
    }
}
