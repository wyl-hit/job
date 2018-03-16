package processor;

import setting.Configs;
import util.DBUtil;
import util.HQuery;

import java.sql.Timestamp;
import java.util.*;


/**
 * Created by wyl on 2017/2/18.
 */
public class CalcWeakTieProcessor implements Runnable {
    public static DBUtil db = null;
    private String source;
    private String user;



    public CalcWeakTieProcessor(String source, String user) {

        this.source = source;
        this.user = user;
        this.db = new DBUtil(source);

    }

    @Override
    public void run() {
        // TODO Auto-generated method stub

        Timestamp timeRange = new Timestamp(System.currentTimeMillis());
        timeRange.setMonth(timeRange.getMonth() - 24);
        try {
            updateWeaktie(this.source, this.user, timeRange);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void updateWeaktie(String source, String userId, Timestamp timeRange) {
//        System.out.println(table);
//        System.out.println(userId);
//        System.out.println(after);

        /*
        * 获取用户所有微博id
        * */
        HQuery User2Origin = new HQuery()
                .Select("id", "posttime")
                .From(source + "a")//From("aa")
                .Where("uid = " + userId, "posttime > " + String.valueOf(timeRange.getTime()));


        ArrayList<ArrayList<String>> origins = User2Origin.Query();
        int strong_number = 0;
        Map<String, Integer> fanShareCountMap = new HashMap<String, Integer>();//转发统计
        String strong_link = "";
        for (ArrayList<String> origin : origins) {
//            System.out.println("frommid = " + origin.get(0));
            HQuery Origin2Repost = new HQuery()
                    .Select("toid")
                    .From(source + "c")//From("ac")
                    .Where("frommid = " + origin.get(0), "posttime < 9999999999998");//);
//            System.out.println("ajsajkergkj"+origin.get(1));
            ArrayList<ArrayList<String>> reposts = Origin2Repost.Query();
            for (ArrayList<String> repost : reposts) {
                //根据toid统计转发次数...
                String toId = repost.get(0);
//                System.out.println(repost);
                if (fanShareCountMap.containsKey(toId)) {
                    fanShareCountMap.put(toId, fanShareCountMap.get(toId) + 1);
                } else {
                    fanShareCountMap.put(toId, 1);
                }
            }
        }

//      按照转发的前10%为强粉
        int strongtieNum = Configs.getStrongTieNum();
        int num = 0;
        List<Map.Entry<String, Integer>> list = new ArrayList<Map.Entry<String, Integer>>(fanShareCountMap.entrySet());
        Collections.sort(list, new Comparator<Map.Entry<String, Integer>>(){
            public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2){
                return o2.getValue() - o1.getValue();
            }
        });

        strong_number = list.size() / 10;

        for(int i = 0; i < strong_number; i++){
                strong_link += "," + list.get(i).getKey();
        }


/*        按照固定的强连接数
//        for (String shareId : fanShareCountMap.keySet()) {
//
//            if (fanShareCountMap.get(shareId) >= strongtieNum) {
//                strong_number++;
//
//                strong_link += "," + shareId;
//            }
//            num++;
//        }
        */

        System.out.println("repostNum " + num);
        if (strong_link.length() > 0)
            strong_link = strong_link.substring(1, strong_link.length() - 1);

        // insert db


        String sqlUpdateUserInfo = "update user set strong_link = ? ,strong_num = ? where uid= ? ";
        List<String> parameters = new ArrayList<String>();
        parameters.clear();
        parameters.add(strong_link);
        parameters.add(String.valueOf(strong_number));
        parameters.add(userId);
        int re = db.update(sqlUpdateUserInfo, parameters);
        db.close();
    }



    //@deprecated
    public void updateWeaktieFan(String userId, Timestamp after) {
        DBUtil db = new DBUtil();
        String strong_link = "";
        int number = 0;
        int strongtieNum = Configs.getStrongTieNum();
        Map<String, Long> fanShareCountMap = new HashMap<String, Long>();
        Map<String, Boolean> fanMap = new HashMap<String, Boolean>();
        String sqlGetFanShareCount = "select c_uid, count(*) as shareNum from repost where from_uid = ? and repost_time > ? GROUP BY c_uid";
        List<String> parameters = new ArrayList<String>();
        parameters.add(userId);
        parameters.add(after.toString());
        List result = null;
        result = db.query(sqlGetFanShareCount, parameters);
        for (Object R : result) {
            fanShareCountMap.put(((Map<String, String>) R).get("c_uid"), ((Map<String, Long>) R).get("shareNum"));
        }
        for (String shareId : fanShareCountMap.keySet()) {
            if (fanShareCountMap.get(shareId) >= strongtieNum) {
                number++;
                strong_link += "," + shareId;
            }

        }
        System.out.println(strong_link);
        if (strong_link.length() > 0)
            strong_link = strong_link.substring(1, strong_link.length() - 1);

        // insert db
        String sqlUpdateUserInfo = "update user set strong_link = ? ,strong_num = ? where uid= ? ";
        parameters.clear();
        parameters.add(strong_link);
        parameters.add(String.valueOf(number));
        parameters.add(userId);
        int re = db.update(sqlUpdateUserInfo, parameters);
        db.close();
    }


    public static void main(String... args) {
//        schedule.WeakTieThread a = new schedule.CalcWeakTieProcessor("a", "101772207");
//////		List<String> users = a.getusers();
//        Timestamp t = new Timestamp(System.currentTimeMillis());
//        t.setMonth(t.getMonth() - 7);
//        a.updateWeaktie("a", "101772207", t);
        Timestamp t = new Timestamp(System.currentTimeMillis());
        t.setMonth(t.getMonth() - 6);

        CalcWeakTieProcessor calcWeakTieProcessor = new CalcWeakTieProcessor("a", "2289674265");
        calcWeakTieProcessor.updateWeaktie("a", "2289674265", t);


    }


}




