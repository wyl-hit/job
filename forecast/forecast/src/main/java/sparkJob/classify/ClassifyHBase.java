package sparkJob.classify;

//import org.ansj.domain.Result;
import org.ansj.domain.Term;
import org.ansj.splitWord.analysis.ToAnalysis;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import org.apache.spark.api.java.function.Function;
import org.apache.spark.ml.Pipeline;
import org.apache.spark.ml.PipelineModel;
import org.apache.spark.ml.PipelineStage;
import org.apache.spark.ml.classification.DecisionTreeClassifier;
import org.apache.spark.ml.feature.*;
import org.apache.spark.mllib.classification.LogisticRegressionModel;
import org.apache.spark.mllib.classification.LogisticRegressionWithLBFGS;
import org.apache.spark.mllib.evaluation.MulticlassMetrics;
import org.apache.spark.mllib.linalg.*;
import org.apache.spark.mllib.regression.LabeledPoint;
import org.apache.spark.sql.DataFrame;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SQLContext;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.Metadata;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import scala.Tuple2;

import java.io.IOException;
import java.util.*;

import java.io.Serializable;

/**
 * Created by wyl on 2017/2/15.
 */
public class ClassifyHBase {
    //private ToAnalysis analysis = new ToAnalysis();
    private final static String symbol = "[]$^()-=~！@#￥%…&*（）—+·{}|：“”《》？：:【】、；‘’，。.,、+";
    private static Set<String> symbolChar = null;
    static {
        symbolChar = new HashSet<String>();
        for(int i = 0; i< symbol.length(); i++)
        {
            String ch = String.valueOf(symbol.charAt(i));
            symbolChar.add(ch);
        }
    }

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

        //0
        StringIndexerModel labelIndexer = new StringIndexer()
                .setInputCol("label")
                .setOutputCol("indexedLabel")
                .fit(sentenceDataFrame);

        //1
        Tokenizer tokenizer = new Tokenizer().setInputCol("sentence").setOutputCol("words");

        //2
        List<String> stopList = new ArrayList<String>();
        Object[] obj = stopWords.collect().toArray();
        for(Object o : obj){
            stopList.add(o.toString());
        }
        StopWordsRemover remover = new StopWordsRemover().setStopWords(stopList.toArray(new String[stopList.size()]));
        remover.setInputCol("words").setOutputCol("filtered");

        //3
        int numFeatures = 30000;
        HashingTF hashingTF = new HashingTF().setInputCol("filtered").setOutputCol("rawFeatures").setNumFeatures(numFeatures);


        //4
        IDF idf = new IDF().setInputCol("rawFeatures").setOutputCol("features");
        Pipeline idfpipeline = new Pipeline()
                .setStages(new PipelineStage[]{tokenizer, remover, hashingTF, idf});

        //前期特征完毕
        PipelineModel idfModel = idfpipeline.fit(sentenceDataFrame);
        DataFrame rescalaData = idfModel.transform(sentenceDataFrame);

        DecisionTreeClassifier dt = new DecisionTreeClassifier()
                .setLabelCol("indexedLabel")
                .setFeaturesCol("features");

        JavaRDD<Row> trainingRow = rescalaData.select("label","features").toJavaRDD();
        JavaRDD<LabeledPoint> training = trainingRow.map(
                new Function<Row, LabeledPoint>(){
                    public LabeledPoint call(Row r){
                        int label = r.getInt(0);
                        org.apache.spark.mllib.linalg.Vector v = r.getAs(1);
                        return new LabeledPoint(label, v);
                    }
                });

        JavaRDD<LabeledPoint> training2 = training.sample(false, 0.7);
        training2.cache();

        final LogisticRegressionModel model = new LogisticRegressionWithLBFGS().setNumClasses(15).run(training2.rdd());


        JavaRDD<LabeledPoint> testing = training.subtract(training2);

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


    public static void cutWords(){
        SparkConf conf = new SparkConf().setAppName("JavaRandomForestClassifierExample");
        JavaSparkContext jsc = new JavaSparkContext(conf);
        SQLContext sqlContext = new SQLContext(jsc);
        List<String> sentence = Arrays.asList("在训练场上，即将远赴澳大利亚参加陆军轻武器技能大赛的我国参赛选手正在紧张备战。", "参加这次比赛的一些国家是属于射击俱乐部的专业队，常年备战，实力强悍，想要超越他们，夺得金牌，难度可想而知。 ", "即将出国比赛，集训选手们要做哪些准备？");
        JavaRDD<String> sentenceJDD = jsc.parallelize(sentence);
        JavaRDD<String> wordsJDD = sentenceJDD.map(new Function<String, String>() {
            private static final long serialVersionUID = 1L;
            @Override
            public String call(String s) throws Exception {
                s.replace('\n', ' ').replace('\t', ' ');
                List<Term> cutResultList = ToAnalysis.parse(s);
//                Result cutResultList = analysis.parse(s);
                StringBuffer sff = new StringBuffer();
                for(Term t : cutResultList){
                    String name = t.getName();
                    if(symbolChar.contains(name))
                        continue;
                    sff.append(name).append(" ");
                }
                return sff.toString();
            }
        });
        List<String>words = wordsJDD.collect();
        for(String s: words){
            System.out.println(s);
        }
    }

    public static void main(String[] args){
        cutWords();
    }

}
