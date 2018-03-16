package deprecated;

import setting.Configs;
import util.DBUtil;
import util.activeMQ.Producer;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Created by dapt on 2017/2/20.
 */
public class UpdateTrainFileSender {
    public static final String[] sources = new String[]{
            "a",
            "b",
//			"c",
//			"d"
    };

    public static void sender(String source) {
        Producer producer = new Producer(Configs.TrainQueue);
        DBUtil db = new DBUtil(source);
        List<String> users = new ArrayList<String>();
        String sqlGetusers = "select uid from user";
        List result = null;
        result = db.query(sqlGetusers);
        for (Object R : result) {
            try {
                System.out.println(((Map<String, String>) R).get("uid"));
                producer.sendMessage(source + " " + ((Map<String, String>) R).get("uid"));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        producer.close();
        db.close();
    }

    public static void main(String[] args){
        for(String source : sources)
            sender(source);
    }




}
