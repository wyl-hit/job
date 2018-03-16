package deprecated;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.hbase.Cell;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.DataFrame;
import org.apache.spark.sql.SQLContext;
//import org.apache.hadoop.hbase.spark.JavaHBaseContext;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.*;

import util.HDFSUtil;
import util.HbaseUtil;
import util.UrlUtils;

public class getfeature {
	public static Log log = LogFactory.getLog(getfeature.class);
	
	private static  String MYSQL_CONNECTION_URL = "jdbc:mysql://192.168.18.206:3306/forecast";
    private static  String MYSQL_USERNAME = "root";
    private static  String MYSQL_PWD = "123456";
	
//	private static SparkConf sparkConf = new SparkConf().setAppName("feature");
//	private static JavaSparkContext jsc = new JavaSparkContext(sparkConf);
	public static HbaseUtil hbase = new HbaseUtil().table("forecast").family("message");
	public static UrlUtils u =new UrlUtils();
	
	public static HashMap<Integer, Integer> stage_time = new HashMap<Integer, Integer>(){
		{
			put(1, 3);//3h
			put(2, 6);//6h
			put(3, 12);//12h
			put(4, 24);//24h
			put(5, 72);//72h
			put(6, 168);//168h
			put(7, -1);//不限时间
		}
	};

	
//    JavaHBaseContext hbaseContext = new JavaHBaseContext(jsc, conf);
	
	public static void main(String[] args) throws InterruptedException {
		
		String uidString = "1000005991";
		hbase.close();/* 用完记得close */
    }
	

	
    private static byte[] Trans(String raw) {
        return Bytes.toBytes(raw);
    }
    
	public List<MsgShareDetail> getUserMsgShareDetail(String msgId){
		ResultScanner rs = null;
		List<MsgShareDetail> userMsgShareDetail = new ArrayList<MsgShareDetail>();
		String rowKeyBeginString = "ac_" + msgId + "_0";
		String rowKeyEndString = "ac_" + msgId + "_9";
		rs = hbase.query("forecast", rowKeyBeginString, rowKeyEndString);
		for (Result rlt: rs ) {
			Cell cell_toid = rlt.getColumnLatestCell(Trans("message"), Trans("toid"));
			Cell cell_likenum = rlt.getColumnLatestCell(Trans("message"), Trans("likenum"));
			Cell cell_posttime = rlt.getColumnLatestCell(Trans("message"), Trans("posttime"));
			userMsgShareDetail.add( new MsgShareDetail( 
										CellUtil.cloneValue(cell_toid).toString(), 
										Integer.parseInt(CellUtil.cloneValue(cell_likenum).toString()), 
										new Timestamp(cell_posttime.getTimestamp()) ) );
        }
		return userMsgShareDetail;
	}
    
	public void getEachMsgFeature(String userId) throws Exception{
		Map<String, Timestamp> userMsgPostTime = weibo_user_post(userId);
		HDFSUtil hdfs = new HDFSUtil();
		
		String data = "";
		
		for(String msgId : userMsgPostTime.keySet()){
			Timestamp msgPostTime = userMsgPostTime.get(msgId);
			Timestamp predictTime = msgPostTime;
			List<MsgShareDetail> userMsgShareDetail = getUserMsgShareDetail(msgId);
			List<Integer> feature = new ArrayList<Integer>();
			List<Integer> label = new ArrayList<Integer>();
			
			for(int i = 1; i < 6; i++){
				msgPostTime.setHours(msgPostTime.getHours() + stage_time.get(i));
				predictTime.setHours(msgPostTime.getHours() + stage_time.get(i + 1));
				long weakTieNum = getWeakTieNum(userId, msgId, msgPostTime);
				
				
				int stage_repost_num = 0;
				int stage_like_num = 0;
				int label_repost_num = 0;
				
				for(MsgShareDetail msgShareDetail : userMsgShareDetail){
					if(msgShareDetail.shareTime.before(msgPostTime)){
						stage_like_num += msgShareDetail.likeCount;
						//stage_repost_num += msgShareDetail.shareCount;
						stage_repost_num += 1;
					}
					if(msgShareDetail.shareTime.before(predictTime)){
						//label_repost_num +=  msgShareDetail.shareCount;
						label_repost_num += 1;
					}
				}
				feature.add((int)weakTieNum);
				feature.add(stage_repost_num);
				feature.add(stage_like_num);
				feature.add(0);//记忆效应：设为0
				label.add(label_repost_num);
			}
			
			ArrayList<String> resultFeature = new ArrayList<String>(); 
			
			for(int i = 0; i < 6; i++){
				String rf = "";
				rf = rf + label.get(i) + "\t";
				int j = 0;
				for(j = 0; j < (i + 1)* 4; j++){
					rf = rf + (j + 1) + ":" + feature.get(j) + " ";
				}
				for(int k = j; k < 24; k++){
					rf = rf + k + ":0 ";
				}
				
				rf += "25:0";//影响力
				data += (rf) + "\n";
				resultFeature.add(rf);
			}
			
		}
		data = data.substring(0, data.length() - 1);
		hdfs.writeToHDFS("/user/root/jx/forecast/training/" + userId, data);
		
	}
	
	public static List<String> repostUsercard(String mId, Timestamp msgPostTimeAfterHours){
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
    	Date beginTimestamp = null;
		try {
			beginTimestamp = sdf.parse("2007-01-01 00:00");
		} catch (java.text.ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		List<String> usercard = new ArrayList<String>();
		String rowKeyBeginString = "ac_" + mId + "_" + beginTimestamp.getTime();
		String rowKeyEndString = "ac_" + mId + "_" + msgPostTimeAfterHours.getTime();
		ResultScanner rs = null;
		rs = hbase.query("forecast", rowKeyBeginString, rowKeyEndString);
		for (Result rlt: rs ) {
			Cell cell_id = rlt.getColumnLatestCell(Trans("message"), Trans("id"));
			usercard.add(CellUtil.cloneValue(cell_id).toString());
        }
		return usercard;
	}
    
	private long getWeakTieNum(String userId, String msgId,
			Timestamp msgPostTimeAfterHours) {
		// TODO Auto-generated method stub
		SparkConf conf = new SparkConf().setAppName("readmysqlDF").set("spark.kryoserializer.buffer.max","1g");
		JavaSparkContext sc = new JavaSparkContext(conf);
		SQLContext sqlContext = new SQLContext(sc);
		Properties connectionProperties = new Properties();
		connectionProperties.setProperty("dbtable", "user");
		connectionProperties.setProperty("user", MYSQL_USERNAME);
		connectionProperties.setProperty("password", MYSQL_PWD);
		String[] predicates = {"id='" + userId + "'"};
		DataFrame jbdcDataFrame = sqlContext.read().jdbc(MYSQL_CONNECTION_URL, "user", predicates, connectionProperties).select("StrongLink");
		String fans_id_stringString = jbdcDataFrame.collect()[0].getString(0);
		HashSet<String> StrongLink = new HashSet<String>(Arrays.asList(fans_id_stringString.split(","))); 
		List<String> usercard = repostUsercard(msgId, msgPostTimeAfterHours);
		Long count = new Long(0);
		for(String u : usercard){
			if(StrongLink.contains(u)){
				continue;
			}
				count += 1;
		}
		return count;
	}


	public static Map<String, Timestamp> weibo_user_post(String uidString) {
		// TODO Auto-generated method stub
		String rowKey = "aa" + uidString;
		ResultScanner rs = null;
		Map<String, Timestamp> msgPostTimeMap = new HashMap<String, Timestamp>();
		rs = hbase.query("forecast", rowKey+"_0", rowKey+"_9");
		for (Result rlt: rs ) {
			Cell cell_time = rlt.getColumnLatestCell(Trans("message"), Trans("posttime"));
			Cell cell_id = rlt.getColumnLatestCell(Trans("message"), Trans("id"));
			msgPostTimeMap.put(CellUtil.cloneValue(cell_id).toString(), new Timestamp(cell_time.getTimestamp()));
        }
		return msgPostTimeMap;
	}
   

}
