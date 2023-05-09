﻿using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.IO;
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
using System.Windows.Navigation;
using System.Windows.Shapes;


namespace WindowsApp
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>

    public partial class MainWindow : Window
    {
        public ObservableCollection<string> ListsNames { get; set; } = new ObservableCollection<string>();
        private FileSystemWatcher watcher = new FileSystemWatcher();
        private StocksListDataWindow listDataWindow = null;

        public MainWindow()
        {
            InitializeComponent();
            stocksLists.DataContext = this;

            DirectoryInfo dataDirectory = new DirectoryInfo(Constants.savedDataPath());
            foreach (DirectoryInfo data_directory in dataDirectory.GetDirectories())
            {
                ListsNames.Add(data_directory.Name);
            }

            watcher.Path = Constants.savedDataPath();
            watcher.NotifyFilter = NotifyFilters.DirectoryName;
            watcher.Created += OnFileCreated;
            watcher.Deleted += OnFileDeleted;
            watcher.EnableRaisingEvents = true;

        }

        private void OnFileCreated(object sender, FileSystemEventArgs e)
        {
            App.Current.Dispatcher.Invoke((Action)delegate {
                ListsNames.Add(e.Name);
            });
        }


        private void OnFileDeleted(object sender, FileSystemEventArgs e)
        {
            App.Current.Dispatcher.Invoke((Action)delegate {
                ListsNames.Remove(e.Name);
            });
        }

        private void openExtractWindow_Click(object sender, RoutedEventArgs e)
        {
            NewListWindow newListWindow = new NewListWindow();
            newListWindow.ShowDialog();
        }

        private void DeleteClicked(object sender, RoutedEventArgs e)
        {
            MenuItem menuItem = (MenuItem)sender;
            ContextMenu contextMenu = (ContextMenu)menuItem.Parent;
            ListBoxItem listItem = (ListBoxItem)contextMenu.PlacementTarget;
            string listName = (string)listItem.DataContext;
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
            
        }

        private void FilterClicked(object sender, RoutedEventArgs e)
        {
            MenuItem menuItem = (MenuItem)sender;
            ContextMenu contextMenu = (ContextMenu)menuItem.Parent;
            ListBoxItem listItem = (ListBoxItem)contextMenu.PlacementTarget;
            string listName = (string)listItem.DataContext;
            string listPath = Constants.savedDataPath() + listName + "\\"+ listName;

            if (File.Exists(listPath))
            {
                string parameters = listPath +
                                    " 10";
                string extractStocksExe = System.IO.Path.Combine(Constants.pythonScriptsPath(), "FilterStocks.exe");
                Utils.ExecuteScript(extractStocksExe, parameters);
            }
        }

        private void ShowList(object sender, MouseButtonEventArgs e)
        {
            ListBoxItem listItem = (ListBoxItem)sender;
            string listName = (string)listItem.DataContext;

            if (listDataWindow != null)
            {
                if (listDataWindow.ShowActivated == false)
                    listDataWindow.Show();
                else
                    listDataWindow.Close();
            }

            try
            {
                listDataWindow = new StocksListDataWindow(listName);
                listDataWindow.Closing += (s, args) => listDataWindow = null;
                listDataWindow.Show();
            }
            catch(InitializetionFailed ex) { }
        }
    }
}
