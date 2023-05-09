using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WindowsApp
{
    internal static class Utils
    {
        public static void ExecuteScript(string script, string parameters)
        {
            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.FileName = "CMD.EXE";
            startInfo.Arguments = "/K " + script + " " + parameters;
            startInfo.WindowStyle = ProcessWindowStyle.Normal;

            Process proc = new Process();
            proc.StartInfo = startInfo;
            proc.Start();
        }
    }
}
