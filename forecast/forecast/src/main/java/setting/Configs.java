package setting;

import java.util.Map;
import java.util.HashMap;

/** 
 *  @Project: forecast
 *	@Title: Configs.java
 *	@Author: jx
 *  @Date: Sep 8, 2016 7:27:10 AM
 * 	@Description: TODO
 *  @Version: v1.0
 */
public class Configs {


	public static void main(String[] args){
//		String[] r = "   dfd df ".split("\\s+",0);
//		System.out.println(r[0]);
//		System.out.println(r[1]);
//		System.out.println(r[2]+ "d");
//		System.out.println(r[3] + "d");
//		System.out.println(r[4]);

	}
	
	public static final Map<String, String> dbConfig = new HashMap<String, String>(){
		{
			put("url", "jdbc:mysql://192.168.18.206:3306/shcrawler?zeroDateTimeBehavior=convertToNull&useUnicode=true&characterEncoding=utf8");
			put("driver", "com.mysql.jdbc.Driver");
			put("user", "root");
			put("password", "123456");
			put("batchNum", "1000");
			put("tableWeibo", "shcrawler");
			put("tableTwitter", "twitter_data");
			put("tableFacebook", "facebook_data");
			put("tableTieba", "tieba_data");
			put("customUrl", "jdbc:mysql://192.168.18.206:3306/");
			put("options", "?zeroDateTimeBehavior=convertToNull&useUnicode=true&characterEncoding=utf8");

//			put("url", "jdbc:mysql://192.168.18.206:3306/shcrawler?zeroDateTimeBehavior=convertToNull&useUnicode=true&characterEncoding=utf8");
			//test
//			put("url", "jdbc:mysql://localhost:3306/test");
//			put("driver", "com.mysql.jdbc.Driver");
//			put("user", "root");
//			put("password", "root");
			
		}
	};
	public static Map<String, String> hadoopConfig = new HashMap<String, String>(){
		{
//			put("host", "master");
//			put("hdfshost", "hdfs://192.168.91.129:9000/");
//			put("host", "192.168.8.157");
			put("hdfshost", "hdfs://192.168.18.206");
		}
	};
	
	public static Map<String, String> sparkConfig = new HashMap<String, String>(){
		{
			put("sparkMaster", "spark://master:7077");
		}
	};
	
	public static Map<String, Integer> StrongTieNum = new HashMap<String, Integer>(){
		{
			put("strongTieNum", 5);
		}
	};
	
	
	public static String getDBUrl(){
		return dbConfig.get("url");
	}
	public static String getDBDriver(){
		return dbConfig.get("driver");
	}
	public static String getDBUser(){
		return dbConfig.get("user");
	}
	public static String getDBPassword(){
		return dbConfig.get("password");
	}
	public static String getBatchNum(){
		return dbConfig.get("batchNum");
	}
	




	/*
	* 训练预测的hdfs文件路径
	* */
	public static String predictPrefixPath = "/user/root/jx/forecast/predict/";
	public static String trainPrefixPath = "/user/root/jx/forecast/training/";
	public static String modelPrefixPath = "/user/root/jx/forecast/model/";

	/*
	* 训练预测特征选择列
	* */
	public static String[] cols = new String[]{
			"result",
			"likenum",
			"commentnum",
			"repostnum",
			"stronglikenum",
			"strongcommentnum",
			"strongrepostnum",
			"memoryeffect"
	};


//	public static String getHadoopHost(){
//		return hadoopConfig.get("host");
//	}
	public static String getHadoopHDFSHost(){
		return hadoopConfig.get("hdfshost");
	}
	
	public static String getSparkMaster(){
		return sparkConfig.get("sparkMaster");
	}
	
	public static Integer getStrongTieNum(){
		return StrongTieNum.get("strongTieNum");
	}

	/**
	 * 各个Processor的线程数量
	 */
	public static final int NWeakTie = 30;
	public static final int NCalcFeature = 20;
	public static final int NDetectPredict = 1;
	public static final int NTain = 10;


	/**
	 * 对于所有的worker，从MQ中取消息的速度远远高于处理消息的速度，
	 * 对于每个消息都会生成一个线程处理任务，而线程池的线程数量有限，所以会造成大量线程处于等待队列，
	 * 即：又在本机中形成了一个“MQ”，主线程终止后随即丢失，不利于调试，且造成系统资源浪费。
	 * 所以每次取消息时,检查线程池是否已满，满了则主线程等待，暂缓取消息创建新任务
	 * 根据消息处理的速度为主线程设置适当的等待时间（单位：ms）
	 */
	public static final int MainThreadWaitTime = 150;

	//队列名称
	public static final String FeatureQueue = "Forecast_CalcFeatureQ";
	public static final String WeaktieQueue = "Forecast_WeakTieQ";
	public static final String PredictQueue = "Forecast_PredictQ";
	public static final String TrainQueue = "Forecast_TrainQ";



	/**
	 * HBase数据库属性的配置
	 */
	public static final String tableName = "forecast";
	public static final String familyMessage = "message";
	public static final String familyPredict = "predict";
	public static final String familyUser = "user";

	/**
	 * 时间节点的配置
	 */
	//实际的
	public static final int NCheckPoint = 6;//关键的时间节点个数
	public static final int CheckPoint[] = new int[]{0, 3, 6, 24, 72, 168};//关键的时间节点（按小时计算）
	
	
	
}
