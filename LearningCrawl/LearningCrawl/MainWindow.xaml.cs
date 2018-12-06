using System;
using System.Windows;
using System.Windows.Controls;
using LearningCrawl.Tools;
using Newtonsoft.Json.Linq;

namespace LearningCrawl
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow
    {
        private int _count;
        private JArray _subject = new JArray();
        public MainWindow()
        {
            InitializeComponent();
        }

        private async void ButtonBase_OnClick(object sender, RoutedEventArgs e)
        {
            Requests s = new Requests();
            Button2.Content = "获取中";
            Button2.IsEnabled = false;
            PgBar2.Visibility = Visibility.Visible;
            PgBar2.IsIndeterminate = true;
            try
            {
                string a = await s.Get($"http://api.douban.com/v2/movie/in_theaters?start={_count}");
                JObject jo = JObject.Parse(a);
                _count += (int)jo["count"];
                _subject.Merge(jo["subjects"]);
                foreach (JToken joEach in jo["subjects"])
                {
                    ListBox2.Items.Add($"[{joEach["rating"]["average"]}/{joEach["rating"]["max"]}] {joEach["title"]}");
                }
            }
            catch (Exception exception)
            {
                Label2.Content = exception.Message;
                Button2.IsEnabled = true;
                Button2.Content = "重新获取";
            }
            Button2.IsEnabled = true;
            Button2.Content = "继续获取";
            PgBar2.IsIndeterminate = false;
            PgBar2.Visibility = Visibility.Collapsed;
        }

        private void Button3_Click(object sender, RoutedEventArgs e)
        {
            Window2 window2 = new Window2();
            window2.setSubject(_subject);
            Close();
            window2.Show();
        }
        private void ListBox2_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            MessageBox.Show(ListBox2.SelectedItem.ToString(), _subject[ListBox2.SelectedIndex]["title"].ToString());
        }
    }
}