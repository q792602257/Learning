using System;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using SYNCTRLLib;

namespace ConsoleApplication11
{
    internal class Program
    {
        private static readonly SynAPICtrl api = new SynAPICtrl();
        private static readonly SynDeviceCtrl device = new SynDeviceCtrl();
        private static readonly SynPacketCtrl packet = new SynPacketCtrl();
        private static int deviceHandle;
        public static int x = Screen.PrimaryScreen.Bounds.Width;
        public static int y = Screen.PrimaryScreen.Bounds.Height;
        public static float Xmin, Xmax, Ymin, Ymax;

        [DllImport("user32.dll")]
        private static extern bool SetCursorPos(int X, int Y);

        private static void Main(string[] args)
        {
            try
            {
                api.Initialize();
            }
            catch (Exception e)
            {
                Console.WriteLine(
                    "Error calling API, you didn't have Synaptics hardware or driver (if you just installed it you need to reboot)");
                loop:
                Console.WriteLine("Press enter to quit OR type \"info\"");
                if (Console.ReadLine().Contains("info"))
                {
                    Console.WriteLine("{0} Exception caught.", e);
                    goto loop;
                }

                return;
            }

            api.Activate();
            //select the first device found
            deviceHandle = api.FindDevice(SynConnectionType.SE_ConnectionAny, SynDeviceType.SE_DeviceTouchPad, -1);
            device.Select(deviceHandle);
            device.Activate();
            device.OnPacket += SynTP_Dev_OnPacket;
            Console.Title = Assembly.GetExecutingAssembly().GetName().Name;
            Console.SetWindowSize(58, 9);
            Console.SetBufferSize(58, 9);
            Console.ReadLine();
        }

        private static void SynTP_Dev_OnPacket()
        {
            var result = device.LoadPacket(packet);
            if (packet.X > 1)
            {
                Console.SetCursorPosition(0, 2);
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, 2);
                Console.WriteLine("X:" + packet.X + " Y:" + packet.Y);
                Xmin = 1600;
                Xmax = 5400;
                Ymin = 1300;
                Ymax = 4000;

//                if (Xmin == 0 && Xmax == 0)
//                {
//                    Xmin = packet.X;
//                    Xmax = packet.X;
//                    Ymin = packet.Y;
//                    Ymax = packet.Y;
//                }
//                if (packet.X > 1)
//                {
//                    if (Xmin > packet.X)
//                        Xmin = packet.X;
//                    if (Xmax < packet.X)
//                        Xmax = packet.X;
//                }
//                if (packet.Y > 1)
//                {
//                    if (Ymin > packet.Y)
//                        Ymin = packet.Y;
//                    if (Ymax < packet.Y)
//                        Ymax = packet.Y;
//                }
                var targetx = (packet.X - Xmin) / (Xmax - Xmin) * x;
                var targety = (Ymax - Ymin - (packet.Y - Ymin)) / (Ymax - Ymin) * y;
                SetCursorPos((int) targetx, (int) targety);
                ;
                Console.WriteLine("Xmin:" + Xmin + " Ymin:" + Ymin);
                Console.WriteLine("Xmax:" + Xmax + " Ymax:" + Ymax);
                Console.SetCursorPosition(0, 6);
                Console.Write(new string(' ', Console.WindowWidth));
                Console.SetCursorPosition(0, 6);
                Console.WriteLine("X:" + targetx + " Y:" + targety);
            }
        }
    }
}