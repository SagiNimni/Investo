using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using System.Diagnostics;
using System.Threading;
using System.Reflection;


namespace WindowsApp
{
    /// <summary>
    /// Interaction logic for NewListWindow.xaml
    /// </summary>
    public partial class NewListWindow : Window
    {

        public NewListWindow()
        {
            InitializeComponent();
        }

        private void ensureNumbersOnlyTextBox(object sender, TextCompositionEventArgs e)
        {
            Regex _regex = new Regex("[^0-9]+");
            e.Handled = _regex.IsMatch(e.Text); 
        }

        private void Submit_Click(object sender, RoutedEventArgs e)
        {
            //ensure parameters all provided
            if (ListName.Text == "" || YearsBack.Text == "" || ListSize.Text == "" || MarketCap.Text == "")
            {
                MessageBox.Show("Please fill out all the parameters!");
                return;
            }
       
            List<String> checkedSectors = new List<String>();
            string sectors;
            foreach (var sector in Sectors.Children)
            {
                var sectorObj = sector as CheckBox;
                if (sectorObj.IsChecked == true) 
                {
                    checkedSectors.Add(sectorObj.Content.ToString());
                }
            }
            if (checkedSectors.Count == 0)
            {
                MessageBox.Show("There must be at least one sector chosen");
                return;
            }
            else if (checkedSectors.Count == 11)
                sectors = "None";
            else
                sectors = "['" + string.Join("','", checkedSectors) + "']";

            string marketCapParameter = "";
            switch (MarketCap.Text)
            {
                case "Small Caps":
                    marketCapParameter = "'small'";
                    break;
                case "Medium Caps":
                    marketCapParameter = "'medium'";
                    break;
                case "Large Caps":
                    marketCapParameter = "'large'";
                    break;
                case "All Caps":
                    marketCapParameter = "'all'";
                    break;
            }

            // Start proccess 
            string parameters = Constants.savedDataPath() + ListName.Text +
                                " " + YearsBack.Text +
                                " amount_of_stocks=" + ListSize.Text +
                                " extract_market_cap=" + marketCapParameter +
                                " sectors=" + sectors;
            string extractStocksExe = System.IO.Path.Combine(Constants.pythonScriptsPath(), "ExtractStocks.exe");
            ProcessStartInfo startInfo= new ProcessStartInfo();
            startInfo.FileName= "CMD.EXE";
            startInfo.Arguments = "/K " + extractStocksExe + " " + parameters;
            startInfo.WindowStyle = ProcessWindowStyle.Normal;
            
            Process proc = new Process();
            proc.StartInfo = startInfo;
            proc.Start();
            proc.WaitForExit();

            Close();
        } 

        
    }
}
