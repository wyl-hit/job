package sparkJob.forecast;

import org.apache.spark.SparkConf;
import org.apache.spark.SparkException;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.api.java.function.PairFunction;
import org.apache.spark.broadcast.Broadcast;
import org.apache.spark.mllib.linalg.Vector;
import org.apache.spark.mllib.linalg.Vectors;
import org.apache.spark.mllib.regression.LabeledPoint;
import org.apache.spark.mllib.regression.LinearRegressionModel;
import org.apache.spark.mllib.tree.model.GradientBoostedTreesModel;
import org.apache.spark.sql.DataFrame;
import org.apache.spark.sql.DataFrameReader;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SQLContext;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.JavaDStream;
import org.apache.spark.streaming.api.java.JavaPairDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;

import scala.Serializable;
import scala.Tuple2;
import util.HDFSUtil;

import java.io.File;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import setting.Configs;
import util.HbaseUtil;


public class ForecastPredict {
    public static Configs config = new Configs();
    public static String predictPath = Configs.predictPrefixPath;
    public static String modelRootPath = Configs.modelPrefixPath;

    private static String MYSQL_CONNECTION_URL = "jdbc:mysql://192.168.18.206:3306/shcrawler";
    private static String MYSQL_USERNAME = "root";
    private static String MYSQL_PWD = "123456";
    public static HashMap<String, GradientBoostedTreesModel> models = new HashMap<String, GradientBoostedTreesModel>();
    final static SparkConf conf = new SparkConf().setAppName("ForecastPredict");
    final static JavaSparkContext sc = new JavaSparkContext(conf);
    // 创建流式操作对象
    final static JavaStreamingContext ssc = new JavaStreamingContext(sc, Durations.seconds(10));
    // 创建数据库操作对象
    private static final SQLContext sqlContext = new SQLContext(sc);
    private static Broadcast<HashMap<String, GradientBoostedTreesModel>> bc;


    public static HbaseUtil hbase = new HbaseUtil()
            .table("forecast")
            .family("predict");

    public ForecastPredict() {
        this.MYSQL_CONNECTION_URL = config.getDBUrl();
        this.MYSQL_USERNAME = config.getDBUser();
        this.MYSQL_PWD = config.getDBPassword();
    }

    //创建一个 JavaStreamingContext 对象，用来告诉 Spark 如何访问集群
    public static void main(String[] args) throws Exception {
        //将模型加载到内存中并广播到各个worker
//    	config.getDBUrl();
        loadModel();
        bc = sc.broadcast(models);
        //进行监控文件目录，进行预测
        System.out.println("---------------------------------------------------------------------------------------");
        System.out.println("predicting start...");
        System.out.println("---------------------------------------------------------------------------------------");
        forecastStreaming();
        System.out.println("---------------------------------------------------------------------------------------");
        System.out.println("predicting end...");
        System.out.println("---------------------------------------------------------------------------------------");

        ssc.start();
        ssc.awaitTermination();
    }
/*  // 从mysql中read数据
    public static DataFrameReader createSqlObject(){
        DataFrameReader reader = sqlContext.read().format("jdbc");
        reader.option("url",MYSQL_CONNECTION_URL);//数据库路径
        //reader.option("dbtable","zxz_result");  //数据表名
        reader.option("driver","com.mysql.jdbc.Driver");
        reader.option("user",MYSQL_USERNAME);
        reader.option("password",MYSQL_PWD);
        return reader;
    }
*/
/*    public static void loadModel(){
        File file=new File(modelRootPath);
        File[] fileList = file.listFiles();
        if(fileList.length != 0)
        for(File one_file:fileList){
                String model_name = "file://" + modelRootPath + one_file.getName();
                models.put(one_file.getName(), LinearRegressionModel.load(sc.sc(), model_name));
            }
    }
*/




    /**
     * 流式建模
     * 任务格式：<uid-mid, 0, index1:value1...>
     *
     * @description: uid:用户id用于数据库插入标识； mid:微薄id，用于数据库插入标识； 0:默认标签； index1：libsvm数据索引； value1:libsvm数据值
     */
    public static void forecastStreaming() throws Exception {
        String Path = predictPath;
        JavaPairDStream<String, LabeledPoint> predictData = ssc.textFileStream(Path).mapToPair(
                new PairFunction<String, String, LabeledPoint>() {
                    public Tuple2<String, LabeledPoint> call(String line) {
                        String[] parts = line.split(",");
                        if (parts.length < 2) {
                            System.out.println("[ForecastPredict]: task error...");
                            return null;
                        }
                        String svmData = parts[1];
                        String[] data = svmData.split(" ");
                        Double label = Double.parseDouble(data[0]);
                        List<Integer> indices = new ArrayList<Integer>();
                        List<Double> values = new ArrayList<Double>();
                        int Dimensions = 0;
                        int idx = Integer.parseInt(data[1].split(":")[0]);
                        for (int j = 1; j < idx; j++) {
                            indices.add(j);
                            values.add(0.0);
                        }

                        for (int i = 1; i < data.length; i++) {
                            String[] indexAndValue = data[i].split(":");
                            Integer index = Integer.parseInt(indexAndValue[0]);
                            Dimensions = index;

                            Double value = Double.parseDouble(indexAndValue[1]);
                            indices.add(index);
                            values.add(value);
                        }
                        int[] indicesA = new int[indices.size()];
                        for (int i = 0; i < indices.size(); i++) {
                            indicesA[i] = indices.get(i);
                        }
                        double[] valuesA = new double[values.size()];
                        for (int i = 0; i < values.size(); i++) {
                            valuesA[i] = values.get(i);
                        }

                        LabeledPoint feature = new LabeledPoint(label, Vectors.sparse(Dimensions, indicesA, valuesA));

                        return new Tuple2<String, LabeledPoint>(parts[0], feature);
                    }
                }).cache();

        predictData.foreachRDD(new Function<JavaPairRDD<String, LabeledPoint>, Void>() {
            public Void call(JavaPairRDD<String, LabeledPoint> tasks) throws Exception {
//                    if(!prdd.collect().isEmpty()){
//                    List<Tuple2<String, LabeledPoint>> tasks = ;
                for (Tuple2<String, LabeledPoint> one_task : tasks.collect()) {
                    String source = one_task._1().split("-")[0];
                    String uid = one_task._1().split("-")[1];//
                    String mid = one_task._1().split("-")[2];
                    String stage = one_task._1().split("-")[3];
                    HashMap<String, GradientBoostedTreesModel> temphm = bc.value();
//                    System.out.println(temphm.size());
                    System.out.println(one_task._1());
                    System.out.println(one_task._2().features());
                    System.out.println(source + "e" + uid + "_" + mid);
                    System.out.println(String.valueOf(Integer.valueOf(stage) + 1) + "predict");

                    if (temphm.get(source + "-" +  uid) != null) {
                        double prediction = temphm.get(source + "-" + uid).predict(one_task._2().features());


//                        Connection conn2mysql = null;
//                        Statement statement = null;
                        try {
//                            Class.forName("com.mysql.jdbc.Driver").newInstance();
//                            conn2mysql = DriverManager.getConnection(MYSQL_CONNECTION_URL, MYSQL_USERNAME, MYSQL_PWD);
//                            statement = conn2mysql.createStatement();
                            //String sql="update zxz_result set nPredict='"+prediction+"' where uid='"+uid+"'and mid='"+mid+"'";
//                            String sql = "update model_predict set " + stage + "predict=" + prediction + " where uid='" + uid + "'and wid='" + mid + "'";
                            hbase.replaceInsert(
                                    "forecast",
                                    "predict",
                                    source + "e" + uid + "_" + mid,
                                    Arrays.asList(String.valueOf(stage + 1) + "predict"),
                                    Arrays.asList(String.valueOf(prediction))
                            );
                            System.out.println(source + "e" + uid + "_" + mid);
                            System.out.println(prediction);


                        } catch (Exception e) {
                            e.printStackTrace();
                        } finally {

//                            if (conn2mysql != null) {
//                                try {
//                                    conn2mysql.close();
//                                } catch (SQLException e) {
//                                    e.printStackTrace();
//                                }
//                            }
//                            if (statement != null) {
//                                try {
//                                    statement.close();
//                                } catch (SQLException e) {
//                                    e.printStackTrace();
//                                }
//                            }
                        }
//                        }
//                        else{
//                            System.out.println("no model");
//                        }
                    }
                }

                return null;
            }
        });


    }

    /**
     * 将svm数据的字符串解析成LabeledPoint
     */
    public static LabeledPoint parseSVM(String svmData) {
        String[] data = svmData.split(" ");
        Double label = Double.parseDouble(data[0]);
        List<Integer> indices = new ArrayList<Integer>();
        List<Double> values = new ArrayList<Double>();
        int Dimensions = 0;
        int idx = Integer.parseInt(data[1].split(":")[0]);
        for (int j = 1; j < idx; j++) {
            indices.add(j);
            values.add(0.0);
        }

        for (int i = 1; i < data.length; i++) {
            String[] indexAndValue = data[i].split(":");
            Integer index = Integer.parseInt(indexAndValue[0]);
            Dimensions = index;

            Double value = Double.parseDouble(indexAndValue[1]);
            indices.add(index);
            values.add(value);
        }
        int[] indicesA = new int[indices.size()];
        for (int i = 0; i < indices.size(); i++) {
            indicesA[i] = indices.get(i);
        }
        double[] valuesA = new double[values.size()];
        for (int i = 0; i < values.size(); i++) {
            valuesA[i] = values.get(i);
        }
        return new LabeledPoint(label, Vectors.sparse(Dimensions, indicesA, valuesA));

    }

    public static void loadModel() {


        HDFSUtil hdfs = new HDFSUtil();
        List<String> fileList = hdfs.getHDFSFile(modelRootPath);
        for (String one_file : fileList) {
            String model_name = modelRootPath + one_file;
            models.put(one_file, GradientBoostedTreesModel.load(sc.sc(), model_name));
        }
    }






    public static void forecastStreamingt() throws Exception {
        String Path = predictPath;
        JavaPairDStream<String, LabeledPoint> predictData = ssc.textFileStream(Path).mapToPair(
                new PairFunction<String, String, LabeledPoint>() {
                    public Tuple2<String, LabeledPoint> call(String line) {
                        String[] parts = line.split(",");
                        if (parts.length < 2) {
                            System.out.println("[ForecastPredict]: task error...");
                            return null;
                        }

                        String svmData = parts[1];
                        String[] data = svmData.split(" ");
                        Double label = Double.parseDouble(data[0]);
                        List<Integer> indices = new ArrayList<Integer>();
                        List<Double> values = new ArrayList<Double>();
                        int Dimensions = 0;
                        int idx = Integer.parseInt(data[1].split(":")[0]);
                        for (int j = 1; j < idx; j++) {
                            indices.add(j);
                            values.add(0.0);
                        }

                        for (int i = 1; i < data.length; i++) {
                            String[] indexAndValue = data[i].split(":");
                            Integer index = Integer.parseInt(indexAndValue[0]);
                            Dimensions = index;

                            Double value = Double.parseDouble(indexAndValue[1]);
                            indices.add(index);
                            values.add(value);
                        }
                        int[] indicesA = new int[indices.size()];
                        for (int i = 0; i < indices.size(); i++) {
                            indicesA[i] = indices.get(i);
                        }
                        double[] valuesA = new double[values.size()];
                        for (int i = 0; i < values.size(); i++) {
                            valuesA[i] = values.get(i);
                        }

                        LabeledPoint feature = new LabeledPoint(label, Vectors.sparse(Dimensions, indicesA, valuesA));


                        return new Tuple2<String, LabeledPoint>(parts[0], feature);
                    }
                }).cache();

//        predictData.foreachRDD(new Function<JavaPairRDD<String, LabeledPoint>, Void>(){
//			public Void call(JavaPairRDD<String, LabeledPoint> o) throws Exception{
//				for(Tuple2<String, LabeledPoint> t : o.collect()){
//					System.out.println(t._1());
//					System.out.println(t._2());
//				}
//				return null;
//			}
//		});

        predictData.foreachRDD(new Function<JavaPairRDD<String, LabeledPoint>, Void>() {
            public Void call(JavaPairRDD<String, LabeledPoint> tasks) throws Exception {
//                    if(!prdd.collect().isEmpty()){
//                    List<Tuple2<String, LabeledPoint>> tasks = ;
                for (Tuple2<String, LabeledPoint> one_task : tasks.collect()) {
                    System.out.println(one_task._1());
//
                }
//                    }
                return null;
            }
        });
    }


}