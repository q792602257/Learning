import java.util.Date;
import java.text.SimpleDateFormat;
public class HW {
    public static void main(String[] args) {
        for(int i = 0;i<100;i++){
            SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            System.out.printf("Now Time is : %s\n",df.format(new Date()));
            try{Thread.sleep(1000);}
            catch(InterruptedException e){return;}
        }
    }
}
