using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Policy;
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
    /// Interaction logic for StockGradesWindow.xaml
    /// </summary>
    /// 
    class Scale
    {
        private float value;
        private string name;

        public Scale(float value, string name)
        {
            this.value = value;
            this.name = name;
        }
    }


    public partial class StockGradesWindow : Window
    {
        public StockGradesWindow()
        {
            InitializeComponent();
        }
    }
}
