package processor;

import org.apache.activemq.command.ActiveMQObjectMessage;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.client.Result;
import setting.Configs;
import util.FileUtil;
import util.HDFSUtil;
import util.HbaseUtil;
import util.HQuery;

import java.lang.reflect.Array;
import java.util.*;

public class FeaturePredictProcessor implements Runnable {

    String source = null;
    String uid = null;
    String msgId = null;
    int stage = 0;


    private static String[] cols = Arrays.copyOfRange(Configs.cols, 1, Configs.cols.length);

    public FeaturePredictProcessor(String source, String uid, String msgid, int stage) {
        this.source = source;
        this.uid = uid;
        this.msgId = msgid;
        this.stage = stage;
    }

    public static void main(String[] args) {
        FeaturePredictProcessor f = new
                FeaturePredictProcessor("a", "2709577332", "4057781742366800", 2);
        f.readHBase2HDFS("a", "2709577332", "4057781742366800", 2);
    }


    /*
    * 读取HBase中的特征数据到HDFS文件中
    * 预测流使用
    * feature: uid-mid-stage,0 index1:value1 ....
    * 0作为默认label
    * */
    public void readHBase2HDFS(String source, String uid, String msgid, int stage) {
        if(stage > 5){
            return ;
        }

        HbaseUtil hb = new HbaseUtil();
        HDFSUtil hdfs = new HDFSUtil();


        String rowKey = source + "e" + uid + "_" + msgid;
        Result result = hb.query("forecast", rowKey);
        List<Cell> cells = result.listCells();

        String feature = source +"-"+ uid + "-" + msgid + "-" + stage + ",0";
        Map<String, String> featureMap = new HashMap<>();
        hb.print(result);
        for (Cell cell : cells) {
            featureMap.put(hb.Trans(CellUtil.cloneQualifier(cell)), hb.Trans(CellUtil.cloneValue(cell)));
        }
        hb.close();

        int i = 1;
        for (i = 1; i <= stage; i++) {
            for (int j = 0; j < cols.length; j++) {
                if (featureMap.containsKey(i + cols[j]) && !"".equals(featureMap.get(i + cols[j]))) {
//                    String tmp = ;
//                        tmp = tmp.;
                    feature += " " + (j + 1 + (i - 1) * cols.length) + ":" + featureMap.get(i + cols[j]).replace(" ","").replace(",","");
                } else {
                    feature += " " + (j + 1 + (i - 1) * cols.length) + ":0";
                }
            }
        }

        for (; i < 6; i++) {
            for (int j = 0; j < cols.length; j++) {
                feature += " " + (j + 1 + (i - 1) * cols.length) + ":0";
            }
        }





        System.out.println(feature);
        try {
            hdfs.writeToHDFS(Configs.predictPrefixPath + String.valueOf(System.currentTimeMillis()) + "_" + uid + ".data", feature);
        } catch (Exception e) {
            e.printStackTrace();
        }

    }


    @Override
    public void run() {
        // TODO Auto-generated method stub
        try {
            readHBase2HDFS(this.source, this.uid, this.msgId, this.stage);
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

}
