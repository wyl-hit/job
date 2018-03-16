package tmp;

import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import util.HbaseUtil;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by dapt on 2017/2/22.
 */
public class queryResult {


    /*
    * @param:source->爬虫通道："a","b","c","d"
    * uid->用户id
    * @return：用户的特征列表，每个数据一行（x,y），用\t分隔
    * */
    public static List<String> getResult(String source, String uid){
        HbaseUtil hb = new HbaseUtil();
        String startrowKey = source + "e" + uid + "^";
        String stopRowKey = source + "e" + uid + "`";
        ResultScanner resultScanner = hb.query("forecast", startrowKey, stopRowKey);

        List<String> rs = new ArrayList<>();
        List<String> cols = new ArrayList<String>() {
            {
                add("repostnum");
                add("weakdivall");
                add("lnrepostnum");
            }
        };


        for(Result result: resultScanner) {
            List<Cell> cells = result.listCells();
            Map<String, String> featureMap = new HashMap<>();
//            hb.print(result);
            String row = null;
            for (Cell cell : cells) {
                featureMap.put(hb.Trans(CellUtil.cloneQualifier(cell)), hb.Trans(CellUtil.cloneValue(cell)));
                row = hb.Trans(CellUtil.cloneRow(cell));
            }

            String repostnum3 = featureMap.get("3result");
//            String weakdivall3 = featureMap.get("3weakdivall");
            String lnweakdivall3 = featureMap.get("3lnweakdivall");
//            String repostnum6 = featureMap.get("6result");
            String lnrepostnum6 = featureMap.get("6lnrepostnum");
//            String mid = featureMap.get("mid")

            if(!"0".equals(repostnum3))
                System.out.println(row + "\t" +lnweakdivall3 + "\t" + lnrepostnum6);

//            if(!"0".equals(repostnum3))
//                rs.add(lnweakdivall3 + "\t" + lnrepostnum6);
        }

        hb.close();
        return rs;
    }



    public static void main(String[] args){
        String source = "a";
        String uid = UID.uid;
        getResult(source, uid);
//        feature = feature.substring(0, feature.length() - 1);



    }




}
