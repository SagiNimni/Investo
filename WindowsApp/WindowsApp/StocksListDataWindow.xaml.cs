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
using System.Text.RegularExpressions;
using System.Threading;
using System.Windows.Threading;

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
        private FileSystemWatcher watcher = new FileSystemWatcher();
        public ObservableCollection<string> stockNames { get; set; } = new ObservableCollection<string>();

        private string listName;
        private string json_path;
        private string sorting_path;
        private Dictionary<string, Ratios> listData;


        public StocksListDataWindow(string listName)
        {   
            InitializeComponent();
            this.listName = listName;
            DataContext = this;

            this.json_path = Constants.savedDataPath() + listName + "\\" + listName + ".json";
            this.sorting_path = Constants.savedDataPath() + listName + "\\sorted.json";

            try
            {


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

                listData = readDataFromJson<Ratios>(json_path);

                string[] sort = null;
                if (File.Exists(sorting_path))
                    sort = readDataFromJson<float>(sorting_path).Keys.ToArray();
                else
                    sort = listData.Keys.ToArray();

                foreach (string symbol in sort)
                {
                    stockNames.Add(symbol);
                }
            }

            catch (Exception ex)
            {
                MessageBox.Show("Failed to open this list");
                throw new InitializetionFailed("Failed to open the stock's list", ex);
            }


            watcher.Path = Constants.savedDataPath() + listName;
            watcher.Filter = "sorted.json";
            watcher.NotifyFilter = NotifyFilters.LastWrite;
            watcher.Changed += new FileSystemEventHandler(OnNewSort);
            watcher.EnableRaisingEvents = true;
        }

        public string getListName()
        {
            return this.listName;
        }

        private void OnNewSort(object sender, FileSystemEventArgs e)
        {
            System.Windows.Application.Current.Dispatcher.Invoke(() => this.stockNames.Clear());

            foreach (string symbol in readDataFromJson<float>(sorting_path).Keys)
            {
                System.Windows.Application.Current.Dispatcher.Invoke(() => this.stockNames.Add(symbol));
            }


        }

        private Dictionary<string, T> readDataFromJson<T>(string fileName)
        {

            using (FileStream fs = new FileStream(fileName, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
            using (StreamReader reader = new StreamReader(fs))
            {
                string json = reader.ReadToEnd();
                dynamic data = JsonConvert.DeserializeObject<dynamic>(json);

                Dictionary<string, T> dict = new Dictionary<string, T>();
                foreach (JProperty property in data)
                {
                    string company = property.Value.Path;
                    company = company.Replace("[", "").Replace("]", "").Replace("'", "");

                    dict.Add(company, property.Value.ToObject<T>());
                }

                return dict;
            }

        }

        private void FilterList()
        {
            string listPath = Constants.savedDataPath() + listName;

            if (System.IO.File.Exists(listPath))
            {
                string parameters = listPath +
                                    " 10";
                string extractStocksExe = System.IO.Path.Combine(Constants.pythonScriptsPath(), "FilterStocks.exe");
                Utils.ExecuteScript(extractStocksExe, parameters);

            }
        }

        private void SortClicked(object sender, RoutedEventArgs e)
        {
            SortOptions optionsPage = new SortOptions(this);
            optionsPage.Show();
        }

        private void DeleteClicked(object sender, RoutedEventArgs e)
        {
            string listPath = Constants.savedDataPath() + listName;

            if (Directory.Exists(listPath))
            {
                DirectoryInfo dir = new DirectoryInfo(listPath);
                foreach (FileInfo file in dir.EnumerateFiles())
                {
                    file.Delete();
                }
                dir.Delete();
            }

            Close();
        }

        private void ShowStockValues(object sender, MouseButtonEventArgs e)
        {
            ListBoxItem listItem = (ListBoxItem)sender;
            string stockName = (string)listItem.DataContext;

            dynamic values = listData[stockName];
        }
    }
}
