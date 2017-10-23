import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class socket {
	protected static String api(int no){
        String[] send={"uptime","isNginx","isMysql","dfStat","memStat"};
        return "jerryadmin{\"method\":\""+send[no]+"\"}1";
    }
	public String sendData(Socket s,String data) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		PrintWriter write = new PrintWriter(s.getOutputStream());
		write.printf(data);
		write.flush();
		BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
		String recv = new String("");
		String info = new String("");
		while((info=in.readLine())!=null){
			recv += info;
			System.out.println(info);
		}
		return recv;
	}
	public static void main(String args[]) throws IOException {
		Socket s = new Socket("64.137.206.200", 8888);
		String send = api(0);
		System.out.println(send);
		String recv = new socket().sendData(s,send);
		System.out.printf(recv);
		s.close();
	}
}
