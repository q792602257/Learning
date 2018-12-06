using System;
using System.Linq;
using System.Windows;
using System.Windows.Input;
using Newtonsoft.Json.Linq;

namespace LearningCrawl
{
    public partial class Window2
    {
        private JToken _subject;
        public Window2()
        {
            InitializeComponent();
        }

        public void setSubject(JToken jToken)
        {
            _subject = jToken;
            Label3.Content = $"Set!{jToken.Count()}";
        }

        private void Label3_OnMouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            Window _upperWindow = new MainWindow();
            _upperWindow.Show();
            Close();
        }
    }
}
