package tmp;

/**
 * Created by dapt on 2017/2/22.
 */
public class UID {
    public static String uid =
    "1730077315";
//            "1223762662";
//        "5187664653";


    public static void main(String[] args){
        int count = 30;
        while(true){
            if(count-- > 20){
                continue;
            }
            if(count < 0){
                break;
            }
        }
    }
}
