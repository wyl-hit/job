package processor;

import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import util.DBUtil;
import util.HDFSUtil;
import util.HQuery;
import util.HbaseUtil;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by wyl on 2017/2/20.
 */
public class UpdateTrainFileProcessor implements Runnable {

    private String source = null;
    private String uid = null;


    public UpdateTrainFileProcessor(String source, String uid) {
        this.source = source;
        this.uid = uid;
    }


    public static void updateFeatureFile(String uid) {

    }

    /*
    * 一个用户的一条消息的标签与特征向量
    * label index1:value1
    * @deprecated
    * */
//    public String getFeature(String source, String uid, String msgid, int stage) {
//        HbaseUtil hb = new HbaseUtil();
//        String rowKey = source + "e" + uid + "_" + msgid;
//        Result result = hb.query("forecast", rowKey);
//        if (result.isEmpty()) {
//            return "";
//        }
//        List<Cell> cells = result.listCells();
//        Map<String, String> featureMap = new HashMap<>();
////        hb.print(result);
//        for (Cell cell : cells) {
//            featureMap.put(hb.Trans(CellUtil.cloneQualifier(cell)), hb.Trans(CellUtil.cloneValue(cell)));
//        }
//        hb.close();
//        String feature = featureMap.get(stage + "result") + " ";//init = label
//
//        List<String> cols = new ArrayList<String>() {
//            {
//                add("likenum");
//                add("commentnum");
//                add("repostnum");
//                add("stronglikenum");
//                add("strongcommentnum");
//                add("strongrepostnum");
//                add("memoryeffect");
//            }
//        };
//
//        for (int i = 1; i <= stage; i++) {
//            for (int j = 0; j < cols.size(); j++) {
//                if (featureMap.containsKey(i + cols.get(j))) {
//                    if ("".equals(featureMap.get(i + cols.get(j)))) {
////                        featureMap.put(i + cols.get(j), "0");
//                        continue;
//                    }
//                    feature += (j + 1 + (i - 1) * cols.size()) + ":" + featureMap.get(i + cols.get(j)) + " ";
//                }
//            }
//        }
//
//        return feature;
//    }

    /*
    * 更新一个用户的模型特征文件
    * @param：source->通道 uid->用户id
    * @deprecated
    * */
//    public void updateFeatureFile(String source, String uid) {
//        HDFSUtil hdfs = new HDFSUtil();
//
//
//        //查询所有的消息id
//        HQuery User2Origin = new HQuery()
//                .Select("id", "posttime")
//                .From(source + "a")//From("aa")
//                .Where("uid = " + uid, "posttime > 0");
//        ArrayList<ArrayList<String>> origins = User2Origin.Query();
//        String allFeature = "";
////        System.out.println(origins);
//        for (ArrayList<String> origin : origins) {
//            String msgid = origin.get(0);
//            System.out.println("msg= " + msgid);
//            if (msgid.contains("_M_")) {
//                continue;
//            }
////            String feature = "";
//            for (int stage = 1; stage < 7; stage++) {
//
//                System.out.println("allfeature = " + allFeature);
//                allFeature += getFeature(source, uid, msgid, stage);
//            }
//        }
//        System.out.println(allFeature);
//
//
//        try {
//            hdfs.writeToHDFS(source + uid + "", allFeature);
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//    }



    /*
    * 一次获取一个用户所有的特征数据，包括每条微博所有时间节点数据
    * 特征文件与msgid无关
    * */
    public void getFeature(String source, String uid, String msgid) {
        HbaseUtil hb = new HbaseUtil();
        String startrowKey = source + "e" + uid + "^";
        String stopRowKey = source + "e" + uid + "`";
        ResultScanner resultScanner = hb.query("forecast", startrowKey, stopRowKey);

        List<String> cols = new ArrayList<String>() {
            {
                add("likenum");
                add("commentnum");
                add("repostnum");
                add("stronglikenum");
                add("strongcommentnum");
                add("strongrepostnum");
                add("memoryeffect");
            }
        };

        String feature = "";

        for(Result result: resultScanner) {
            List<Cell> cells = result.listCells();
            Map<String, String> featureMap = new HashMap<>();
//            hb.print(result);

            for (Cell cell : cells) {
                featureMap.put(hb.Trans(CellUtil.cloneQualifier(cell)), hb.Trans(CellUtil.cloneValue(cell)));
            }


            String oneFeature = "";
            for(int stage = 1; stage < 7; stage++){

                String label = featureMap.get(stage + "result");
                if(label == null) continue;
                oneFeature = label + " ";//init = label

                for (int i = 1; i <= stage; i++) {
                    for (int j = 0; j < cols.size(); j++) {
                        if (featureMap.containsKey(i + cols.get(j)) && !"".equals(featureMap.get(i + cols.get(j)))) {
                            oneFeature += (j + 1 + (i - 1) * cols.size()) + ":" + featureMap.get(i + cols.get(j)) + " ";
                        }
                    }
                }
                feature += oneFeature + "\n";
            }
        }

        hb.close();
        System.out.println("feature= " + feature);
        feature = feature.substring(0, feature.length() - 1);










        HDFSUtil hdfs = new HDFSUtil();
        try {
            hdfs.writeToHDFS(source + uid + "", feature);
        } catch (Exception e) {
            e.printStackTrace();
        }


    }







    public static void main(String[] args) {


        UpdateTrainFileProcessor updateTrainFileProcessor = new UpdateTrainFileProcessor("a", "1032404935");
        updateTrainFileProcessor.getFeature("a", "1032404935","");
    }

    public void run() {
//        updateFeatureFile(this.source, this.uid);
    }
}
