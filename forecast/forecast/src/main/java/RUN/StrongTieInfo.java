package RUN;

import org.apache.hadoop.hbase.util.Hash;
import util.DBUtil;

import java.sql.ResultSet;
import java.util.HashMap;
import java.util.HashSet;

/**
 * Created by timz on 2017/2/17.
 */
public class StrongTieInfo {
    /**
     * 获取强连接信息，并存储，减少数据库的读取次数
     */
    public static final String[] sources = new String[]{
            "a",
            "b"
//            , "c"
//            , "d"
    };
    //所有通道的所有用户的所有强粉丝列表
    //<source,<UID,<[StrongFans]>>>
    public static HashMap<String, HashMap<String, HashSet<String>>>
            StrongTieInfo = getStrong();

    synchronized
    public static HashMap<String, HashMap<String, HashSet<String>>> getStrong() {
        HashMap<String, HashMap<String, HashSet<String>>> ret = new HashMap<>();
        for (String source : sources) {
            DBUtil db = new DBUtil(source);
            //加入一条（仅初始化的）通道，稍后加入数据
            HashMap<String, HashSet<String>> users = new HashMap<>();
            ret.put(source, users);
            try {
                String sql = "select uid,strong_link from user ";
                ResultSet rs = db.rawquery(sql);
                while (null != rs && rs.next()) {
                    String uid = rs.getString("uid");
                    String rawlist = rs.getString("strong_link");
                    String[] strongs = rawlist.split(",");
                    //加入一个（仅初始化的）用户，稍后加入数据
                    HashSet<String> strongset = new HashSet<String>();
                    ret.get(source).put(uid, strongset);
                    for (String strong : strongs)
                        //加入强连接用户
                        ret.get(source).get(uid).add(strong);

                }



                db.close();

            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                db.close();
            }
        }System.out.println(ret.get("a").get("1730077315"));
        return ret;
    }

    public static void main(String... args) {
        try {
            System.out.println(StrongTieInfo);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}