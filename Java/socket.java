import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class socket {
	protected String api(int no){
        String[] send={"uptime","isNginx","isMysql","dfStat","memStat"};
        return "jerryadmin{\"method\":\""+send+"\"}";
    }
	public void main() throws IOException {
		Socket s = new Socket("64.137.206.200", 8888);
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		PrintWriter write = new PrintWriter(s.getOutputStream());
		String send = this.api(0);
		write.printf(send);
		write.flush();
		BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
		String info = null;
		while((info=in.readLine())!=null){
			String context=info.substring(10,info.length()-1);
  			System.out.printf(context);
		}
		s.close();
	}
}
