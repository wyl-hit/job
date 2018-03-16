package tmp;

import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.iq80.leveldb.DB;
import util.DBUtil;
import util.HbaseUtil;
import util.activeMQ.Producer;

import java.util.*;

/**
 * Created by dapt on 2017/2/21.
 */
public class CalcFeatureSender {

    public static final String[] sources = new String[]{
            "a",
            "b",
//			"c",
//			"d"
    };

    public static void main(String[] args) {

        for (String source : sources) {
            DBUtil db = new DBUtil(source);
            String sql = "select uid,strong_num from user order by strong_num desc";

            List result = db.query(sql);
            for (Object m : result) {
                Map r = (Map) m;
                System.out.println(r.get("uid"));
                messages(source, r.get("uid").toString());
            }


            db.close();
        }

//                messages("1223762662");
    }


    public static List<String> messages(String source, String uid) {
//        Producer producer = new Producer("tmp1_Forecast_CalcFeatureQ");
//        String uid = UID.uid;


        HbaseUtil hb = new HbaseUtil();
        String startrowKey = source + "a" + uid + "^";
        String stopRowKey = source + "a" + uid + "`";
        ResultScanner resultScanner = hb.query("forecast", startrowKey, stopRowKey);


        List<String> messages = new ArrayList<>();
        for (Result result : resultScanner) {
            List<Cell> cells = result.listCells();
            String rowkey = hb.Trans(CellUtil.cloneRow(cells.get(0)));

            rowkey = rowkey.substring(2);

            String[] splits = rowkey.split("_");
            for (int i = 1; i < 7; i++) {
                String message = source + " " + String.valueOf(i) + " " + splits[0] + " " + splits[2] + " " + splits[1];
//                producer.sendMessage(message);
                messages.add(message);

            }
        }
        hb.close();



//        DBUtil db = new DBUtil(source);
//        String sql = "select id, post_time from weibo where uid = " + uid + " order by post_time desc";
//        List result = db.query(sql);
//
//        for (Object m : result) {
//
//            Map r = (Map) m;
//            String id = (String) r.get("id");
//            String[] idl = id.split("_");
//            String tid = UrlUtils.Uid2Mid(idl[2]);
//
//            if (!r.containsKey("post_time")) {
//                continue;
//            }
//            System.out.println("abc" + r.get("post_time") + "dbf");
//            if (r.get("post_time") == null || r.get("post_time").equals("null")) {
//                continue;
//            }
//
//            String post_time = (r.get("post_time")).toString();
////            System.out.println(r.get("id"));
//
//            System.out.println(post_time);
//            for (int i = 1; i < 7; i++) {
//                String message = source + " " + String.valueOf(i) + " " + uid + " " + tid + " " + post_time;
////                producer.sendMessage(message);
//                messages.add(message);
//
//            }
//        }
//        db.close();
//        producer.close();
        return messages;
    }


}
