using System.IO;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace LearningCrawl.Tools
{
    public class Requests
    {
        public async Task<string> Get(string uri)
        {
            string Html;
            WebRequest req = WebRequest.Create(uri);
            req.Method = "GET";
            req.Headers.Add("Accept-Encoding", "Deflate");
            req.Headers.Add("UserAgent", "Mozilla/4.0");
            WebResponse res = await req.GetResponseAsync();
            using (Stream Stream_Receive = res.GetResponseStream())
            {
                using (StreamReader Stream_Reader = new StreamReader(Stream_Receive, Encoding.Default))
                {
                    Html = Stream_Reader.ReadToEnd();
                }
            }

            return Html;
        }
    }
}