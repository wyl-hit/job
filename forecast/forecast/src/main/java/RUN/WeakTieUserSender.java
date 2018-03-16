package RUN;

import util.DBUtil;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import util.activeMQ.Producer;
import setting.Configs;

/**
 * Created by d3 on 2017/2/17.
 */
public class WeakTieUserSender {

    public static final String[] sources = new String[]{
            "a",
            "b",
//			"c",
//			"d"
    };

//    //获取微博用户表
//    public static List<String> getUsers(){
//        DBUtil db = new DBUtil("b");
//        List<String> users = new ArrayList<String>();
//        String sqlGetusers = "select * from user";
//        List result = null;
//        result = db.query(sqlGetusers);
//        for(Object R : result){
//            users.add(((Map<String, String>)R).get("uid"));
//
//        }
//        db.close();
//        return users;
//    }


    public static void sender(String source) {
        Producer producer = new Producer(Configs.WeaktieQueue);
        DBUtil db = new DBUtil(source);
        List<String> users = new ArrayList<String>();
        String sqlGetusers = "select uid from user";
        List result = null;
        result = db.query(sqlGetusers);
        for (Object R : result) {
            try {
                System.out.println(source + " " + ((Map<String, String>) R).get("uid"));
                producer.sendMessage(source + " " + ((Map<String, String>) R).get("uid"));

            } catch (Exception e) {
                e.printStackTrace();
            }

        }
        producer.close();
        db.close();

    }


    public static void main(String[] args) {
        for(String source : sources)
            sender(source);
//        Producer producer = new Producer(Configs.WeaktieQueue);
//        List<String> users = getUsers();
//
//        try {
//            for (String user : users) {
//                producer.sendMessage(user);
//            }
//        } catch(Exception e){
//            // TODO
//            e.printStackTrace();
//        } finally {
//            producer.close();
//        }
//
    }

}
