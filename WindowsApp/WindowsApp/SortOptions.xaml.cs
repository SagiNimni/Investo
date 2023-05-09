using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
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

namespace WindowsApp
{
    /// <summary>
    /// Interaction logic for SortOptions.xaml
    /// </summary>
    public partial class SortOptions : Window
    {
        private StocksListDataWindow parentWindow;

        public SortOptions(StocksListDataWindow parentWindow)
        {
            InitializeComponent();
            this.Owner = parentWindow; 
            this.parentWindow = this.Owner as StocksListDataWindow;
        }
        
        private void SubmitClicked(object sender, RoutedEventArgs e)
        {
            string parameters = Constants.savedDataPath() + this.parentWindow.getListName() + " " +
                                FilterRatio.Text + " "  +
                                FilterType.Text;
            string FilterByRatiosExe = System.IO.Path.Combine(Constants.pythonScriptsPath(), "FilterByRatios.exe");
            Utils.ExecuteScript(FilterByRatiosExe, parameters);

            Close();
        }
    }
}
