package sparkJob.forecast;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableInputFormat;
import org.apache.hadoop.hbase.protobuf.ProtobufUtil;
import org.apache.hadoop.hbase.protobuf.generated.ClientProtos;
import org.apache.hadoop.hbase.util.Base64;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.spark.SparkConf;
import org.apache.spark.mllib.regression.LinearRegressionModel;
import org.apache.spark.mllib.regression.LinearRegressionWithSGD;
import org.apache.spark.mllib.tree.GradientBoostedTrees;
import org.apache.spark.mllib.tree.configuration.BoostingStrategy;
import org.apache.spark.mllib.tree.model.GradientBoostedTreesModel;
import org.apache.spark.mllib.util.MLUtils;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.broadcast.Broadcast;
import org.apache.spark.mllib.linalg.Vectors;
import org.apache.spark.mllib.regression.LabeledPoint;

import java.util.HashMap;
import java.util.Map;

import org.apache.spark.sql.DataFrame;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SQLContext;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.Metadata;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import scala.Tuple2;

import org.apache.spark.api.java.function.Function2;
import org.apache.spark.api.java.function.PairFunction;

import util.HDFSUtil;

import java.io.File;
import java.util.*;
import java.lang.System;

import static setting.Configs.NCheckPoint;
import static setting.Configs.CheckPoint;
import static util.HbaseUtil.Trans;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;


import setting.Configs;

//$example off$

/**
 * @Project: forecast
 * @Title: Test.java
 * @Author: wyl
 * @Date: Dec 20, 2016 10:52:39 PM
 * @Description: TODO
 * @Version: v1.0
 */
public class ForecastBuildModel {


    public static SparkConf sparkConf = new SparkConf()
            .setMaster("local")
            .setAppName("ForecastBuildModel")
            .set("spark.driver.memory", "64g");


    public static JavaSparkContext sc = new JavaSparkContext(sparkConf);
    public static Configuration conf = null;

    static {
        conf = HBaseConfiguration.create();
        conf.set("hbase.zookeeper.quorum",
                "192.168.18.206,192.168.18.207,192.168.18.208");
        conf.set("hbase.zookeeper.property.clientPort", "2181");
        conf.set("hbase.master", "hdfs://192.168.18.206:60000");
        conf.set("hbase.root.dir", "hdfs://192.168.18.206:9000/hbase");
        conf.set("hbase.client.keyvalue.maxsize", "524288000");
    }

    public static List<String> fileNameList = new ArrayList<String>();
    public static List<String> modelNameList = new ArrayList<String>();
    public static String trainRootPath = Configs.trainPrefixPath;
    public static String modelRootPath = Configs.modelPrefixPath;
    public static int numIterations = 100;
    public static double stepSize = 0.00000001;
    //创建一个 JavaStreamingContext 对象，用来告诉 Spark 如何访问集群
    private static Broadcast<List<String>> bc;

    private static HDFSUtil hdfs = new HDFSUtil();

    private static String[] stage = new String[]{"1", "2", "3", "4", "5", "6"};
    private static String[] cols = Configs.cols;


    public static void main(String[] args) throws Exception {
//	    	String line = "0 128:51 129:159 130:253 131:159 132:50 155:48 156:238 157:252 158:252 159:252 160:237 182:54 183:227 184:253 185:252 186:239 187:233 188:252 189:57 190:6 208:10 209:60 210:224 211:252 212:253 213:252 214:202 215:84 216:252 217:253 218:122 236:163 237:252 238:252 239:252 240:253 241:252 242:252 243:96 244:189 245:253 246:167 263:51 264:238 265:253 266:253 267:190 268:114 269:253 270:228 271:47 272:79 273:255 274:168 290:48 291:238 292:252 293:252 294:179 295:12 296:75 297:121 298:21 301:253 302:243 303:50 317:38 318:165 319:253 320:233 321:208 322:84 329:253 330:252 331:165 344:7 345:178 346:252 347:240 348:71 349:19 350:28 357:253 358:252 359:195 372:57 373:252 374:252 375:63 385:253 386:252 387:195 400:198 401:253 402:190 413:255 414:253 415:196 427:76 428:246 429:252 430:112 441:253 442:252 443:148 455:85 456:252 457:230 458:25 467:7 468:135 469:253 470:186 471:12 483:85 484:252 485:223 494:7 495:131 496:252 497:225 498:71 511:85 512:252 513:145 521:48 522:165 523:252 524:173 539:86 540:253 541:225 548:114 549:238 550:253 551:162 567:85 568:252 569:249 570:146 571:48 572:29 573:85 574:178 575:225 576:253 577:223 578:167 579:56 595:85 596:252 597:252 598:252 599:229 600:215 601:252 602:252 603:252 604:196 605:130 623:28 624:199 625:252 626:252 627:253 628:252 629:252 630:233 631:145 652:25 653:128 654:252 655:253 656:252 657:141 658:37"
//+ "1 159:124 160:253 161:255 162:63 186:96 187:244 188:251 189:253 190:62 214:127 215:251 216:251 217:253 218:62 241:68 242:236 243:251 244:211 245:31 246:8 268:60 269:228 270:251 271:251 272:94 296:155 297:253 298:253 299:189 323:20 324:253 325:251 326:235 327:66 350:32 351:205 352:253 353:251 354:126 378:104 379:251 380:253 381:184 382:15 405:80 406:240 407:251 408:193 409:23 432:32 433:253 434:253 435:253 436:159 460:151 461:251 462:251 463:251 464:39 487:48 488:221 489:251 490:251 491:172 515:234 516:251 517:251 518:196 519:12 543:253 544:251 545:251 546:89 570:159 571:255 572:253 573:253 574:31 597:48 598:228 599:253 600:247 601:140 602:8 625:64 626:251 627:253 628:220 653:64 654:251 655:253 656:220 681:24 682:193 683:253 684:220";
//	    	System.out.println(parseSVM(line));
//
//        buildModelWhole("a");
        buildModelWhole("b");
    }


    //对于wholeTextFiles， 需要实现loadLibSVMFile方法，解析svmfile格式数据
    //wholeTextFiles对于大量的小文件效率比较高，大文件效果没有那么高 返回《文件名：文件内容》
    // 训练模型，如果模型存在则删除后重建
    public static void buildModelWhole(String source) throws Exception {

        Logger.getLogger("org.apache.spark").setLevel(Level.WARN);
        Logger.getLogger("org.eclipse.jetty.server").setLevel(Level.OFF);

        final String modelPath = modelRootPath;

        Configuration conf = HBaseConfiguration.create();
        conf.set("hbase.zookeeper.quorum", "192.168.18.206,192.168.18.207,192.168.18.208");

        conf.set("hbase.zookeeper.property.clientPort", "2181");
        conf.set("hbase.master", "hdfs://192.168.18.206:60000");
        conf.set("hbase.root.dir", "hdfs://192.168.18.206:9000/hbase");
        conf.set("hbase.client.keyvalue.maxsize", "524288000");


        /**
         * 设置hbase的scan
         */
        String StartRow = source + "e/";
        String StopRow = source + "e{";
        Scan scan = new Scan();
        scan.setStartRow(Bytes.toBytes(StartRow));
        scan.setStopRow(Bytes.toBytes(StopRow));
        scan.addColumn(Trans("predict"), Trans("uid"));
        for (String stg : stage)
            for (String col : cols)
                scan.addColumn(Trans("predict"), Trans(stg + col));
        String tableName = "forecast";
        conf.set(TableInputFormat.INPUT_TABLE, tableName);
        ClientProtos.Scan proto = ProtobufUtil.toScan(scan);
        String ScanToString = Base64.encodeBytes(proto.toByteArray());
        conf.set(TableInputFormat.SCAN, ScanToString);
        JavaPairRDD<ImmutableBytesWritable, Result> queryRDD =
                sc.newAPIHadoopRDD(conf, TableInputFormat.class,
                        ImmutableBytesWritable.class, Result.class);

        /**
         * 获取所有阶段的特征数据（每条原文1行）
         */
//        JavaRDD<Tuple2<String, List<String>>> rawFeatureRDD = queryRDD.map(
//                new Function<Tuple2<ImmutableBytesWritable, Result>, Tuple2<String, List<String>>>() {
//                    @Override
//                    public Tuple2<String, List<String>>
//                    call(Tuple2<ImmutableBytesWritable, Result> result)
//                            throws Exception {
//                        String uid = Trans(result._2.getValue(
//                                Trans("predict"), Trans("uid")));
//                        String feature = "";
//                        for (String stg : stage) {
//                            for (String col : cols) {
//                                String tmp = Trans(result._2.getValue(Trans(
//                                        "predict"), Trans(stg + col)));
//                                if (tmp == null)
//                                    feature += "0 ";
//                                else if (tmp.equals(""))
//                                    feature += "0 ";
//                                else
//                                    feature += tmp + " ";
//                            }
//                        }
//                        feature += "\n";
////                        System.out.print(feature);
//                        return new Tuple2<>(uid, Arrays.asList(feature));
//                    }
//                }
//        );
        JavaPairRDD<String, List<String>> rawFeatureRDD = queryRDD.mapToPair(new PairFunction<Tuple2<ImmutableBytesWritable, Result>, String, List<String>>() {
            @Override
            public Tuple2<String, List<String>> call(Tuple2<ImmutableBytesWritable, Result> result) throws Exception {
                String uid = Trans(result._2.getRow()).split("_")[0].substring(2);
//                String uid = Trans(result._2.getValue(
//                        Trans("predict"), Trans("uid")));
                String feature = "";
                for (String stg : stage) {
                    for (String col : cols) {
                        String tmp = Trans(result._2.getValue(Trans(
                                "predict"), Trans(stg + col)));
                        if (tmp == null)
                            feature += "0 ";
                        else if (tmp.equals(""))
                            feature += "0 ";
                        else
                            feature += tmp + " ";
                    }
                }
                feature += "\n";
//                        System.out.print(feature);
                return new Tuple2(uid, Arrays.asList(feature));
            }
        });
//rawFeatureRDD.reduce(new Function2<Tuple2<String, String>, Tuple2<String, String>, Tuple2<String, String>>() {
//    @Override
//    public Tuple2<String, String> call(Tuple2<String, String> stringStringTuple2, Tuple2<String, String> stringStringTuple22) throws Exception {
//
//
//
//
//        return null;
//    }
//})

        JavaPairRDD<String, List<String>> tmpfeatureRDD = rawFeatureRDD.reduceByKey(new Function2<List<String>, List<String>, List<String>>() {
            @Override
            public List<String> call(List<String> strings, List<String> strings2) throws Exception {
//                strings.addAll(strings2);
                List<String> all = new ArrayList<>();
                all.addAll(strings);
                all.addAll(strings2);
                return all;
            }
        });
        JavaRDD<Tuple2<String, List<String>>> featureRDD = tmpfeatureRDD.map(new Function<Tuple2<String, List<String>>, Tuple2<String, List<String>>>() {
            @Override
            public Tuple2<String, List<String>> call(Tuple2<String, List<String>> stringListTuple2) throws Exception {
                return stringListTuple2;
            }
        });
        /**
         * 从中获取各阶段的特征（每条原文分成NCheckPoint - 1 = 5行）
         */
        JavaRDD<Tuple2<String, List<String>>> finalfeatureRDD = featureRDD.map(
                new Function<Tuple2<String, List<String>>, Tuple2<String, List<String>>>() {
                    @Override
                    public Tuple2<String, List<String>> call(Tuple2<String, List<String>> rawAll)
                            throws Exception {
                        List<String> msgFeature = new ArrayList<>();
                        for (String raw : rawAll._2) {
                            final int nFeature = 8;
                            //result Like Comm Rep slike sComm sRep mEffect
                            String[] features = raw.split(" ");
                            for (int stg = 1; stg < NCheckPoint; ++stg) {
                                //result作为label
                                String stgFeature = features[stg * nFeature];
                                int index = 1;
                                int iter = 0;
                                for (iter = 0; iter < stg; ++iter)
                                    for (int inIndex = 1; inIndex < nFeature; ++inIndex)
                                        stgFeature += " " + String.valueOf(index++)
                                                + ":" + features[iter * nFeature + inIndex];
//                            System.out.println(stgFeature);

                                for (; iter < NCheckPoint - 1; ++iter) {

                                    for (int inIndex = 1; inIndex < nFeature; ++inIndex)
                                        stgFeature += " " + String.valueOf(index++)
                                                + ":0";
                                }

                                msgFeature.add(stgFeature);
                            }
                        }
                        return new Tuple2<>(rawAll._1, msgFeature);
                    }
                }
        );
        List<Tuple2<String, List<String>>> modelData = finalfeatureRDD.collect();

//        for(Tuple2<>)


//			JavaPairRDD<String, String> data = sc.wholeTextFiles(trainPath);
//
//
//
//
//	        JavaRDD<Tuple2<String,List<String>>> traindata = data.map(
//	                new Function<Tuple2<String, String>, Tuple2<String, List<String>>>() {
//	                    public Tuple2<String, List<String>> call(Tuple2<String, String> sA) throws Exception {
//	                        String content = sA._2();
//	                        String[] tmpName= sA._1.split("/");
//	                        String fileName = tmpName[tmpName.length-1];
//	                        List<String> ss = Arrays.asList(content.split("\n"));
//	                        return new Tuple2<String, List<String>>(fileName, ss);
//	                    }
//	                }).cache();
//
//	        List<Tuple2<String,List<String>>> modelData = traindata.collect();
        for (Tuple2<String, List<String>> oneData : modelData) {
            JavaRDD<LabeledPoint> DA = sc.parallelize(oneData._2()).map(new Function<String, LabeledPoint>() {
                public LabeledPoint call(String line) {
                    return parseSVM(line);
                }
            }).cache();


//            System.out.println("****************************************************************************");
//            System.out.println(DA.collect().toString());
//            System.out.println("****************************************************************************");

            BoostingStrategy boostingStrategy = BoostingStrategy.defaultParams("Regression");
            boostingStrategy.setNumIterations(10); // Note: Use more iterations in practice.
            boostingStrategy.getTreeStrategy().setMaxDepth(5);
            // Empty categoricalFeaturesInfo indicates all features are continuous.
            Map<Integer, Integer> categoricalFeaturesInfo = new HashMap<Integer, Integer>();
            boostingStrategy.treeStrategy().setCategoricalFeaturesInfo(categoricalFeaturesInfo);


//	            final LinearRegressionModel model =
//	            		LinearRegressionWithSGD.train(JavaRDD.toRDD(DA),numIterations,stepSize);

            final GradientBoostedTreesModel model =
                    GradientBoostedTrees.train(DA, boostingStrategy);


            if (modelNameList.contains(source + "-" + oneData._1())) {
                try {
                    File file = new File(modelRootPath + oneData._1());
                    deleteDir(file);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }


            System.out.println(modelPath + source + "-" + oneData._1);
            try {
                model.save(sc.sc(), modelPath + source + "-" + oneData._1());
            } catch (Exception e) {
                e.printStackTrace();
            }

        }
    }

    // 分批从读取文件，效率较低==训练模型，如果模型存在则删除后重建
    public static void buildModel(String trainPath, String file_name, JavaSparkContext sc) throws Exception {
        try {
            String modelPath = modelRootPath;

//	            JavaRDD<LabeledPoint> trainingData = MLUtils.loadLibSVMFile(sc.sc(), trainPath).toJavaRDD();
            JavaRDD<LabeledPoint> data = MLUtils.loadLibSVMFile(sc.sc(), trainPath).toJavaRDD();

            JavaRDD<LabeledPoint>[] splits = data.randomSplit(new double[]{0.7, 0.3});
            JavaRDD<LabeledPoint> trainingData = splits[0];
            JavaRDD<LabeledPoint> testData = splits[1];

            BoostingStrategy boostingStrategy = BoostingStrategy.defaultParams("Regression");
            boostingStrategy.setNumIterations(3); // Note: Use more iterations in practice.
            boostingStrategy.getTreeStrategy().setMaxDepth(5);
            // Empty categoricalFeaturesInfo indicates all features are continuous.
            Map<Integer, Integer> categoricalFeaturesInfo = new HashMap<Integer, Integer>();
            boostingStrategy.treeStrategy().setCategoricalFeaturesInfo(categoricalFeaturesInfo);

//	            System.out.println("****************************************************************************");
//	            System.out.println(trainingData.collect().toString());
//	            System.out.println("****************************************************************************");


//	            final LinearRegressionModel model =
//	            		LinearRegressionWithSGD.train(JavaRDD.toRDD(trainingData),numIterations,stepSize);

            final GradientBoostedTreesModel model =
                    GradientBoostedTrees.train(trainingData, boostingStrategy);


            //预测结果

            // Evaluate model on test instances and compute test error
            JavaPairRDD<Double, Double> predictionAndLabel =
                    testData.mapToPair(new PairFunction<LabeledPoint, Double, Double>() {
                        @Override
                        public Tuple2<Double, Double> call(LabeledPoint p) {
                            return new Tuple2<Double, Double>(model.predict(p.features()), p.label());
                        }
                    });
            Double testMSE =
                    predictionAndLabel.map(new Function<Tuple2<Double, Double>, Double>() {
                        @Override
                        public Double call(Tuple2<Double, Double> pl) {
                            Double diff = 0.0;
                            if (pl._2() > 1)
                                diff = Math.abs(pl._1() - pl._2()) / pl._2();
                            return diff;
                        }
                    }).reduce(new Function2<Double, Double, Double>() {
                        @Override
                        public Double call(Double a, Double b) {
                            return a + b;
                        }
                    }) / data.count();
            System.out.println("****************************************************************************");
            System.out.println("Test Error -" + file_name + ": " + testMSE);
            System.out.println("Learned classification GBT model:\n" + model.toDebugString());
            System.out.println("****************************************************************************");


            if (modelNameList.contains(file_name)) {
                try {
                    File file = new File(modelRootPath + file_name);
                    deleteDir(file);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }

            model.save(sc.sc(), modelPath + file_name);
        } catch (IllegalStateException e) {
        }
    }

    /**
     * 将svm数据的字符串解析成LabeledPoint
     * label index1:value1 index2:value2 ....
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


    // 返回指定路径下的所有文件的文件名
    public static List<String> getHDFSFile(String path) {
        return hdfs.getHDFSFile(path);
    }

	/*    public static List<String>getFile(String path){

	        ArrayList<String> fileNameList= new ArrayList<String>();
	        File file=new File(path);
	        File[] fileList = file.listFiles();
	        if(fileList.length != 0)
	            for(File one_file:fileList){
	               fileNameList.add(one_file.getName());
	            }
	        return fileNameList;
	    }*/


    // 记录文件发现更新，刚加入的文件列表
    public static List<String> getNewFilePath(File file) {
        File[] fileList = file.listFiles();
        ArrayList<String> newFileList = new ArrayList<String>();
        for (File one_file : fileList) {
            if (!fileNameList.contains(one_file.getName())) {
                fileNameList.add(one_file.getName());
                newFileList.add(one_file.getName());
            }

        }
        return newFileList;
    }

    //遍历删除model 目录
    private static boolean deleteDir(File dir) {
        if (dir.isDirectory()) {
            String[] children = dir.list();
            for (int i = 0; i < children.length; i++) {
                boolean success = deleteDir(new File(dir, children[i]));
                if (!success) {
                    return false;
                }
            }
        }
        // 目录此时为空，可以删除
        return dir.delete();
    }

}
