package sparkJob.classify;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.URI;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Properties;

import scala.Tuple2;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.spark.*;
import org.apache.spark.api.java.*;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.mllib.classification.*;
import org.apache.spark.mllib.evaluation.MulticlassMetrics;
import org.apache.spark.mllib.regression.LabeledPoint;
import org.apache.spark.mllib.tree.RandomForest;
import org.apache.spark.mllib.tree.model.RandomForestModel;
import org.apache.spark.mllib.linalg.Vector;
import org.apache.spark.ml.feature.HashingTF;
import org.apache.spark.ml.feature.IDF;
import org.apache.spark.ml.feature.IDFModel;
import org.apache.spark.ml.feature.StopWordsRemover;
import org.apache.spark.ml.feature.Tokenizer;
import org.apache.spark.sql.DataFrame;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SQLContext;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.Metadata;
import org.apache.spark.sql.types.StructType;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.streaming.*;
import org.apache.spark.streaming.api.java.*;
import org.apache.spark.mllib.linalg.Matrix;
//import org.ansj.domain.Result;
import org.ansj.domain.Term;
import org.ansj.splitWord.analysis.ToAnalysis;  





public class Classify {
	private static  String MYSQL_CONNECTION_URL = "jdbc:mysql://192.168.18.206:3306/forecast";
	private static  String MYSQL_USERNAME = "root";
	private static  String MYSQL_PWD = "123456";

	public static void main(String[] args){
		streamingClassify();
//		classifyModel();
//		System.out.println(cutWords("在训练场上，即将远赴澳大利亚参加陆军轻武器技能大赛的我国参赛选手正在紧张备战。 参加这次比赛的一些国家是属于射击俱乐部的专业队，常年备战，实力强悍，想要超越他们，夺得金牌，难度可想而知。 即将出国比赛，集训选手们要做哪些准备？"));
//		cutwords();
	}

	public static String cutWords(String text){
		ToAnalysis analysis = new ToAnalysis();
		String result = "";
		text.replace('\n', ' ').replace('\t', ' ');
//		Result cutResultList = analysis.parse(text);
		List<Term>cutResultList = analysis.parse(text);
		
		for(Term t : cutResultList){
			String name = t.getName();
			result += name + " ";
		}
		return result;
	}
	
	
	
	
	public static void cutwords(){
		SparkConf conf = new SparkConf().setAppName("calssifyText");
		JavaSparkContext sc = new JavaSparkContext(conf);
		JavaStreamingContext ssc = new JavaStreamingContext(sc, Durations.seconds(10));

		String modelPath = "/user/root/jx/classify/model/classifyModel";
		final String idfModelPath = "/user/root/jx/classify/model/idfModel/idfModel";
		String stopWordPath = "/user/root/jx/classify/data/stopwords.txt";
		String textpath = "/user/root/jx/classify/streamingtext/";
		final List<String> stopList = new ArrayList<String>();
		final LogisticRegressionModel LRModel = LogisticRegressionModel.load(sc.sc(), modelPath);
		
		JavaRDD<String> stopWords = sc.textFile(stopWordPath);
		Object[] obj = stopWords.collect().toArray();
		for(Object o : obj){
			stopList.add(o.toString());
		}
		
		JavaDStream<String> rawStream = ssc.textFileStream(textpath);
		
		rawStream.foreachRDD(new Function<JavaRDD<String>, Void>(){
			public Void call(JavaRDD<String> rdd) throws Exception{
				if(!rdd.isEmpty()){
				SQLContext sqlContext = new SQLContext(rdd.context());
				JavaRDD<Row> rowText = rdd.map(
						new Function<String, Row>(){
							public Row call(String line){
								String[] parts = line.split("\t");
								String words = cutWords(parts[1]);
								return RowFactory.create(parts[0], words);
							}
						});
				StructType schema = new StructType(new StructField[]{
						new StructField("textId", DataTypes.StringType, false, Metadata.empty()),
						new StructField("sentence", DataTypes.StringType, false, Metadata.empty())
				});
				DataFrame sentenceDataFrame = sqlContext.createDataFrame(rowText, schema);
				
				
				Tokenizer tokenizer = new Tokenizer().setInputCol("sentence").setOutputCol("words");
				DataFrame wordsDataFrame = tokenizer.transform(sentenceDataFrame);
				StopWordsRemover remover = new StopWordsRemover().setStopWords(stopList.toArray(new String[stopList.size()]));
				remover.setInputCol("words").setOutputCol("filtered");
				DataFrame filteredDataFrame = remover.transform(wordsDataFrame);

				int numFeatures = 30000;
				HashingTF hashingTF = new HashingTF().setInputCol("filtered").setOutputCol("rawFeatures").setNumFeatures(numFeatures);
				DataFrame featurizedData = hashingTF.transform(filteredDataFrame);
				IDF idf = new IDF().setInputCol("rawFeatures").setOutputCol("features");
				IDFModel idfModel = IDFModel.load(idfModelPath);
				DataFrame reData = idfModel.transform(featurizedData);
				
				JavaRDD<Row> featuresRow = reData.select("textId","features").toJavaRDD();
				
				JavaRDD<Tuple2<String, Vector>> textFeatures = featuresRow.map(
						new Function<Row, Tuple2<String, Vector>>(){
							public Tuple2<String, Vector> call(Row r){
								String textId = r.getString(0);
								Vector v = r.getAs(1);
								return new Tuple2(textId, v);
							}
						});
				textFeatures.cache();
				
				JavaRDD<Tuple2<String,Object>> result = textFeatures.map(
						new Function<Tuple2<String, Vector>, Tuple2<String,Object>>(){
							public Tuple2<String, Object> call(Tuple2<String, Vector> t){
								Double pred = LRModel.predict(t._2);
								return new Tuple2<String, Object>(t._1, pred);
							}
						});
				
				System.out.println(result.collect());
//				writeToLocalFile("/usr/local/test/classify/result", result.collect().toString());
				
				for(Tuple2<String, Object> rs : result.collect()){
					
					String mid = rs._1();
					Object cls = rs._2();
					
					Connection conn2mysql=null;
	                Statement statement =null;
	                try {
	                    Class.forName("com.mysql.jdbc.Driver").newInstance();
	                    conn2mysql = DriverManager.getConnection(MYSQL_CONNECTION_URL, MYSQL_USERNAME, MYSQL_PWD);
	                    statement=conn2mysql.createStatement();
//	                    String sql="update zxz_result set nPredict='"+prediction+"' where uid='"+uid+"'and mid='"+mid+"'";
	                    //String sql="update test set cls = '" + cls + "' where mid = '" + mid +"'";
	                    String sql="update weibo set tag = '" + cls + "' where mid = '" + mid +"'";
	                    statement.execute(sql);

	                } catch (Exception e) {
	                    e.printStackTrace();
	                }finally{
	                    if(conn2mysql !=null){
	                        try {
	                            conn2mysql.close();
	                        } catch (SQLException e) {
	                            e.printStackTrace();
	                        }
	                    }
	                    if(statement !=null){
	                        try {
	                            statement.close();
	                        } catch (SQLException e) {
	                            e.printStackTrace();
	                        }
	                    }
	                }

				}
				
				
								
				
				
				}
				return null;
			}
		});
		
		ssc.start();
		ssc.awaitTermination();
	}
	/** 
	 * 流式分类，使用已建立的模型直接加载，避免建模耗费时间
	 * 将待分类文本导入HDFS classify/text/目录下 Spark自动以流式读取并分类
	*/
	@SuppressWarnings("deprecation")
	public static void streamingClassify(){
		SparkConf conf = new SparkConf().setAppName("calssifyText");
		JavaSparkContext sc = new JavaSparkContext(conf);
		SQLContext sqlContext = new SQLContext(sc);
		JavaStreamingContext ssc = new JavaStreamingContext(sc, Durations.seconds(10));

		String modelPath = "/user/root/jx/classify/model/classifyModel";
		final String idfModelPath = "/user/root/jx/classify/model/idfModel/idfModel";
		String stopWordPath = "/user/root/jx/classify/data/stopwords.txt";
		String textpath = "/user/root/jx/classify/streamingtext/";
		final List<String> stopList = new ArrayList<String>();
		final LogisticRegressionModel LRModel = LogisticRegressionModel.load(sc.sc(), modelPath);
		
		JavaRDD<String> stopWords = sc.textFile(stopWordPath);
		Object[] obj = stopWords.collect().toArray();
		for(Object o : obj){
			stopList.add(o.toString());
		}
		
		JavaDStream<String> rawStream = ssc.textFileStream(textpath);
		
		rawStream.foreachRDD(new Function<JavaRDD<String>, Void>(){
			public Void call(JavaRDD<String> rdd) throws Exception{
				if(!rdd.isEmpty()){
				SQLContext sqlContext = new SQLContext(rdd.context());
				JavaRDD<Row> rowText = rdd.map(
						new Function<String, Row>(){
							public Row call(String line){
								String[] parts = line.split("\t");
								try{
									return RowFactory.create(parts[0], parts[1]);
								} catch (Exception e) {
									// TODO: handle exception
									System.out.println(parts);
									return RowFactory.create(parts[0], "娱乐");
								}
							}
						});
				StructType schema = new StructType(new StructField[]{
						new StructField("textId", DataTypes.StringType, false, Metadata.empty()),
						new StructField("sentence", DataTypes.StringType, false, Metadata.empty())
				});
				DataFrame sentenceDataFrame = sqlContext.createDataFrame(rowText, schema);
				Tokenizer tokenizer = new Tokenizer().setInputCol("sentence").setOutputCol("words");
				DataFrame wordsDataFrame = tokenizer.transform(sentenceDataFrame);
				StopWordsRemover remover = new StopWordsRemover().setStopWords(stopList.toArray(new String[stopList.size()]));
				remover.setInputCol("words").setOutputCol("filtered");
				DataFrame filteredDataFrame = remover.transform(wordsDataFrame);

				int numFeatures = 30000;
				HashingTF hashingTF = new HashingTF().setInputCol("filtered").setOutputCol("rawFeatures").setNumFeatures(numFeatures);
				DataFrame featurizedData = hashingTF.transform(filteredDataFrame);
				IDF idf = new IDF().setInputCol("rawFeatures").setOutputCol("features");
				IDFModel idfModel = IDFModel.load(idfModelPath);
				DataFrame reData = idfModel.transform(featurizedData);
				
				JavaRDD<Row> featuresRow = reData.select("textId","features").toJavaRDD();
				
				JavaRDD<Tuple2<String, Vector>> textFeatures = featuresRow.map(
						new Function<Row, Tuple2<String, Vector>>(){
							public Tuple2<String, Vector> call(Row r){
								String textId = r.getString(0);
								Vector v = r.getAs(1);
								return new Tuple2(textId, v);
							}
						});
				textFeatures.cache();
				
				JavaRDD<Tuple2<String,Object>> result = textFeatures.map(
						new Function<Tuple2<String, Vector>, Tuple2<String,Object>>(){
							public Tuple2<String, Object> call(Tuple2<String, Vector> t){
								Double pred = LRModel.predict(t._2);
								return new Tuple2<String, Object>(t._1, pred);
							}
						});
//				System.out.println("****************************************");
//				System.out.println("****************************************");
//				System.out.println("****************************************");
//				System.out.println(result.collect());
//				writeToLocalFile("/usr/local/test/classify/result", result.collect().toString());
//				System.out.println("****************************************");
//				System.out.println("****************************************");
//				System.out.println("****************************************");
				Connection conn2mysql=null;
                Statement statement =null;
                try {
                    Class.forName("com.mysql.jdbc.Driver").newInstance();
                    conn2mysql = DriverManager.getConnection(MYSQL_CONNECTION_URL, MYSQL_USERNAME, MYSQL_PWD);
                    for(Tuple2<String, Object> rs : result.collect()){
					
                    	String mid = rs._1();
                    	Object cls = rs._2();
                    	try{
                    		statement=conn2mysql.createStatement();
//	                    	String sql="update zxz_result set nPredict='"+prediction+"' where uid='"+uid+"'and mid='"+mid+"'";
                    		//String sql="update test set cls = '" + cls + "' where mid = '" + mid +"'";
                    		String sql="update weibo set type = '" + cls + "' where id = '" + mid +"'";
                    		statement.execute(sql);
                    	} catch (Exception e) {
							// TODO: handle exception
                    		e.printStackTrace();
                    		System.out.println(mid);
						}
                    }

	                } catch (Exception e) {
	                    e.printStackTrace();
	                }finally{
	                    if(conn2mysql !=null){
	                        try {
	                            conn2mysql.close();
	                        } catch (SQLException e) {
	                            e.printStackTrace();
	                        }
	                    }
	                    if(statement !=null){
	                        try {
	                            statement.close();
	                        } catch (SQLException e) {
	                            e.printStackTrace();
	                        }
	                    }
	                }
				
				
								
				
				
				}
				return null;
			}
		});
		
		ssc.start();
		ssc.awaitTermination();
	}
	
	/**
	 * 训练数据在系统运行前上传到HDFS classify/alldata.txt里，停用词表以文件保存在HDFS classify/stopwords.txt里
	 *  分类模型训练，由于分类模型不需要跟新，此代码在系统运行前单独运行，训练得到的模型结果保存在HDFS 目录 classify/model/下
	 * 
	*/
	public static void classifyModel(){
		SparkConf conf = new SparkConf().setAppName("getModel");
		JavaSparkContext sc = new JavaSparkContext(conf);
		SQLContext sqlContext = new SQLContext(sc);
		//HDFSAPI hdfs = new HDFSAPI();
		
		long begin = System.currentTimeMillis();
		
		String path = "/user/root/jx/classify/data/traindata.txt";
		String stopWordPath = "/user/root/jx/classify/data/stopwords.txt";
		String modelpath = "/user/root/jx/classify/model/classifyModel";
		String idfModelPath = "/user/root/jx/classify/model/idfModel/idfModel";
		JavaRDD<String> rawData = sc.textFile(path);
		JavaRDD<String> stopWords = sc.textFile(stopWordPath);
		
		
		JavaRDD<Row> jrdd = rawData.map(
				new Function<String, Row>(){
					public Row call(String line){
						String[] parts = line.split("\t");
						return RowFactory.create(Integer.parseInt(parts[0]),parts[1]);
					}
				});
		StructType schema = new StructType(new StructField[]{
				new StructField("label", DataTypes.IntegerType, false, Metadata.empty()),
				new StructField("sentence", DataTypes.StringType, false, Metadata.empty())
		});
		
		DataFrame sentenceDataFrame = sqlContext.createDataFrame(jrdd, schema);
		
		Tokenizer tokenizer = new Tokenizer().setInputCol("sentence").setOutputCol("words");
		DataFrame wordsDataFrame = tokenizer.transform(sentenceDataFrame);

		List<String> stopList = new ArrayList<String>();
		
		Object[] obj = stopWords.collect().toArray();
		
		for(Object o : obj){
			stopList.add(o.toString());
		}
		StopWordsRemover remover = new StopWordsRemover().setStopWords(stopList.toArray(new String[stopList.size()]));
		remover.setInputCol("words").setOutputCol("filtered");
		DataFrame filteredDataFrame = remover.transform(wordsDataFrame);
		int numFeatures = 30000;
		HashingTF hashingTF = new HashingTF().setInputCol("filtered").setOutputCol("rawFeatures").setNumFeatures(numFeatures);
		DataFrame featurizedData = hashingTF.transform(filteredDataFrame);
		IDF idf = new IDF().setInputCol("rawFeatures").setOutputCol("features");
		IDFModel idfModel = idf.fit(featurizedData);

		DataFrame rescalaData = idfModel.transform(featurizedData);
		
		JavaRDD<Row> trainingRow = rescalaData.select("label","features").toJavaRDD();
		JavaRDD<LabeledPoint> training = trainingRow.map(
				new Function<Row, LabeledPoint>(){
					public LabeledPoint call(Row r){
						int label = r.getInt(0);
						Vector v = r.getAs(1);
						return new LabeledPoint(label, v);
					}
				});
		//training.cache();
		
		JavaRDD<LabeledPoint> training2 = training.sample(false, 0.7);
		training2.cache();
		
		final LogisticRegressionModel model = new LogisticRegressionWithLBFGS().setNumClasses(15).run(training2.rdd());
		
		
		JavaRDD<LabeledPoint> testing = training.subtract(training2);
//		JavaRDD<Tuple2<Double, Double>> valuesAndPreds = testing.map(
//				new Function<LabeledPoint, Tuple2<Double, Double>>(){
//					public Tuple2<Double, Double> call(LabeledPoint l){
//						double prediction = model.predict(l.features());
//						return new Tuple2<Double, Double>(prediction, l.label());
//					}
//				});
		JavaRDD<Tuple2<Object, Object>> valuesAndPreds = testing.map(
				new Function<LabeledPoint, Tuple2<Object, Object>>(){
					public Tuple2<Object, Object> call(LabeledPoint l){
						double prediction = model.predict(l.features());
						return new Tuple2<Object, Object>(prediction, l.label());
					}
				});
		//--------------------------------------------
		long end = System.currentTimeMillis();
		
		
		System.out.println("***********************************************label-pred*******************************************"
			    + valuesAndPreds.collect().toString()
			    + "**********************************************label-pred*******************************************");
		System.out.println("Total Time used:" + (double)(end - begin)/1000 + "s");
		
		MulticlassMetrics metrics = new MulticlassMetrics(valuesAndPreds.rdd());

	    // Confusion matrix
	    Matrix confusion = metrics.confusionMatrix();
	    System.out.println("Confusion matrix: \n" + confusion);

	    // Overall statistics
	    System.out.println("Precision = " + metrics.precision());

		try {
			idfModel.save(idfModelPath);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		model.save(sc.sc(), modelpath);
		
	}
	
	
	public static void classifyText(){
		SparkConf conf = new SparkConf().setAppName("calssifyText");
		JavaSparkContext sc = new JavaSparkContext(conf);
		SQLContext sqlContext = new SQLContext(sc);
		String modelPath = "/user/root/jx/classify/model";
		String stopWordPath = "/user/root/jx/classify/data/stopwords.txt";
		JavaRDD<String> stopWords = sc.textFile(stopWordPath);
		
		final LogisticRegressionModel LRModel = LogisticRegressionModel.load(sc.sc(), modelPath);
		String textpath = "classify/3.txt";
		JavaRDD<String> rawText = sc.textFile(textpath);
		JavaRDD<Row> rowText = rawText.map(
				new Function<String, Row>(){
					public Row call(String line){
						return RowFactory.create(line);
					}
				});
		StructType schema = new StructType(new StructField[]{
				new StructField("sentence", DataTypes.StringType, false, Metadata.empty())
		});
		DataFrame sentenceDataFrame = sqlContext.createDataFrame(rowText, schema);
		Tokenizer tokenizer = new Tokenizer().setInputCol("sentence").setOutputCol("words");
		DataFrame wordsDataFrame = tokenizer.transform(sentenceDataFrame);
		
		List<String> stopList = new ArrayList<String>();
		
		Object[] obj = stopWords.collect().toArray();
		
		for(Object o : obj){
			stopList.add(o.toString());
		}
		

		StopWordsRemover remover = new StopWordsRemover().setStopWords(stopList.toArray(new String[stopList.size()]));
		remover.setInputCol("words").setOutputCol("filtered");
		DataFrame filteredDataFrame = remover.transform(wordsDataFrame);
		

		int numFeatures = 30000;
		HashingTF hashingTF = new HashingTF().setInputCol("filtered").setOutputCol("rawFeatures").setNumFeatures(numFeatures);
		DataFrame featurizedData = hashingTF.transform(filteredDataFrame);
		IDF idf = new IDF().setInputCol("rawFeatures").setOutputCol("features");
		IDFModel idfModel = idf.fit(featurizedData);
		DataFrame reData = idfModel.transform(featurizedData);
		
		JavaRDD<Row> featuresRow = reData.select("features").toJavaRDD();
		JavaRDD<Vector> textFeatures = featuresRow.map(
				new Function<Row, Vector>(){
					public Vector call(Row r){
						return r.getAs(0);
					}
					
				});
		
		textFeatures.cache();
		
		JavaRDD<Double> result = textFeatures.map(
				new Function<Vector, Double>(){
					public Double call(Vector v){
						return LRModel.predict(v);
					}
				});
		
		System.out.println("*******************result*********************");
		System.out.println(result.collect());
		System.out.println("*******************end*********************");
		
		//JavaRDD<Double> result = LRModel.predict(textFeatures);
		
	}
	
	public static void writeToLocalFile(String filePath, String data) throws Exception{
		FileWriter writer = new FileWriter(filePath, false);
		writer.write(data);
		writer.close();
	}
}
