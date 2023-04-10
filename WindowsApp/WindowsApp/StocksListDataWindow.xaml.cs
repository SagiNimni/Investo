using Microsoft.Office.Interop.Excel;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using System.IO;
using Newtonsoft.Json;
using System.Text.Json.Serialization;
using Newtonsoft.Json.Linq;
using System.Collections;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Transactions;

namespace WindowsApp
{
    /// <summary>
    /// Interaction logic for StocksListDataWindow.xaml
    /// </summary>
    /// 
    [Serializable]
    public class InitializetionFailed : Exception
    {
        public InitializetionFailed() : base() { }
        public InitializetionFailed(string message) : base(message) { }
        public InitializetionFailed(string message, Exception inner) : base(message, inner) { }
    }

    class Ratios
    { 
        public dynamic growth { get; set; }
        public dynamic liquidity { get; set; }
        public dynamic leverage { get; set; }
        public dynamic efficiency { get; set; }
        public dynamic profitability { get; set; }
        public dynamic value { get; set; }

    }

    public partial class StocksListDataWindow : System.Windows.Window
    {
        public ObservableCollection<string> stockNames { get; set; } = new ObservableCollection<string>();

        private string listName;
        private Dictionary<string, Ratios> listData;


        public StocksListDataWindow(string listName)
        {   
            InitializeComponent();
            this.listName = listName;
            DataContext = this;

            try
            {
                string json_path = Constants.savedDataPath() + listName + ".json";
                if (!File.Exists(json_path))
                {
                    MessageBoxResult decision = MessageBox.Show("This list is not filtered. Do you want to filter it?", "Confirm Filter", MessageBoxButton.YesNo, MessageBoxImage.Warning);
                    if (decision == MessageBoxResult.Yes)
                    {
                        FilterList();
                    }
                    else
                    {
                        throw new InitializetionFailed("The filtered list doesn't exist");
                    }
                }

                listData = readDataFromJson(json_path);
                foreach (string symbol in (listData.Keys))
                {
                    stockNames.Add(symbol);
                }
            }
            catch(Exception ex)
            {
                MessageBox.Show("Failed to open this list");
                throw new InitializetionFailed("Failed to open the stock's list", ex);
            }
        }

        private Dictionary<string, Ratios> readDataFromJson(string fileName)
        {
            string json = File.ReadAllText(fileName);

            dynamic data = JsonConvert.DeserializeObject<dynamic>(json);

            Dictionary<string, Ratios> dict = new Dictionary<string, Ratios>();
            foreach (JProperty property in data)
            { 
                dict.Add(property.Value.Path, property.Value.ToObject<Ratios>());
            }

            return dict;
        }


        private void FilterList()
        {
                        string listPath = Constants.savedDataPath() + listName;

            if (System.IO.File.Exists(listPath))
            {
                string parameters = listPath +
                                    " 10";
                string extractStocksExe = System.IO.Path.Combine(Constants.pythonScriptsPath(), "FilterStocks.exe");
                ProcessStartInfo startInfo = new ProcessStartInfo();
                startInfo.FileName = "CMD.EXE";
                startInfo.Arguments = "/K " + extractStocksExe + " " + parameters;
                startInfo.WindowStyle = ProcessWindowStyle.Normal;

                Process proc = new Process();
                proc.StartInfo = startInfo;
                proc.Start();
                proc.WaitForExit();
            }
        }

        private void FilterClicked(object sender, RoutedEventArgs e)
        {

        }

        private void DeleteClicked(object sender, RoutedEventArgs e)
        {
            string listPath = Constants.savedDataPath() + listName;

            if (System.IO.File.Exists(listPath))
            {
                System.IO.File.Delete(listPath);
            }

            Close();
        }

        private void ShowStockValues(object sender, MouseButtonEventArgs e)
        {
            ListBoxItem listItem = (ListBoxItem)sender;
            string stockName = (string)listItem.DataContext;

            dynamic values = listData[stockName];
            Console.WriteLine("s");
        }
    }
}
