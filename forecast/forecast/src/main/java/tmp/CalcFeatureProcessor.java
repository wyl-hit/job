package tmp;

import setting.Configs;
import util.HQuery;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import util.activeMQ.Producer;

import static RUN.StrongTieInfo.StrongTieInfo;
import static tmp.CalcFeatureWorker.dbpredict;

/**
 * Created by timz on 2017/2/17.
 */
public class CalcFeatureProcessor implements Runnable {
    private String Source;
    private int Stage;
    private String Uid;
    private String Tid;
    private long PostTime;//timestamp


    public static void main(String[] args) {
        CalcFeatureProcessor cfp = new CalcFeatureProcessor("a 5 1681213010 4076383573234352 1487368800000");
        Thread cfpt = new Thread(cfp);

        ExecutorService ThreadPool = Executors.newFixedThreadPool(2);
        ThreadPool.execute(cfpt);
    }


    public CalcFeatureProcessor(String qdata) {
        /**
         * QDATA : source stage uid tid posttime
         */
        System.out.println("--------------------------------");
        System.out.println("queue data = " + qdata);
        System.out.println("--------------------------------");
        String[] param = qdata.split(" ");
        this.Source = param[0];
        this.Stage = Integer.valueOf(param[1]);
        this.Uid = param[2];
        this.Tid = param[3];
        String postT = param[4];

        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

        if (postT.contains("-")) {
            try {
                postT += " " + param[5];
                Date date = sdf.parse(postT);
//                postT = String.valueOf(date.getTime());
                this.PostTime = date.getTime();
            } catch (Exception e) {
                e.printStackTrace();
            }
        } else {
            this.PostTime = Long.parseLong(postT);
        }
    }

    public void run() {
//        System.out.println(StrongTieInfo.get("a").get("1730077315"));

        //得到原文的一定时间内的转发列表
        Long repostTimestamp = PostTime
                + Configs.CheckPoint[Stage - 1] * 60 * 60 * 1000;
        HQuery OriginToRepost = new HQuery()
                .Select("toid")
                .From(Source + "c")//From("ac")
                .Where("frommid = " + Tid,
                        "posttime < " + String.valueOf(repostTimestamp));
        int strongCount = 0, repostnum = 0;
        ArrayList<ArrayList<String>> reposts = OriginToRepost.Query();
        for (ArrayList<String> repost : reposts) {
            //根据uid、toid判断是否弱连接...
            String toid = repost.get(0);
            ++repostnum;


            //判断是否为强粉
            if (StrongTieInfo.containsKey(Source)) {
                if (StrongTieInfo.get(Source).containsKey(Uid)) {
                    if (StrongTieInfo.get(Source).get(Uid).contains(toid))
                        ++strongCount;
                }
            }



        }


        //强连接数存hbase

        int weakrepostnum = repostnum - strongCount;
        double weakdivall = 0.0;
        if (repostnum > 0) {
            weakdivall = (double) weakrepostnum / (double) repostnum;
        }

        double lnweakdivall = Math.log10(weakdivall);
        double lnrepostnum = Math.log10(repostnum);


        dbpredict.replaceInsert(
                Configs.tableName,
                Configs.familyPredict,
                makePredictRowKey(Source, Uid, Tid),
                makePredictColumns(this.Stage),
                makePredictValues(strongCount, repostnum, weakrepostnum,
                        weakdivall, lnweakdivall, lnrepostnum));

        System.out.println("++++++++++++++++++++++++++++++++++");
        System.out.println("strongCount= " + strongCount);
        System.out.println("weakrepostnum= " + weakrepostnum);
        System.out.println("weakdivall= " + weakdivall);
        System.out.println("lnweakdivall= " + lnweakdivall);
        System.out.println("lnrepostnum= " + lnrepostnum);
        System.out.println("++++++++++++++++++++++++++++++++++" + this.Uid + "  " + this.Tid);

//        Producer predictsender = new Producer(Configs.PredictQueue);
//        predictsender.sendMessage(Source + " "
//                + Uid + " "
//                + Tid + " "
//                + String.valueOf(Stage));
//        predictsender.close();

    }

    private static List<String> makePredictColumns(int stage) {
        List<String> ret = new ArrayList<String>();
        ret.add(String.valueOf(stage + 1) + "strongrepostnum");
        ret.add(String.valueOf(stage + 1) + "result");
        ret.add(String.valueOf(stage + 1) + "weakrepostnum");
        ret.add(String.valueOf(stage + 1) + "weakdivall");
        ret.add(String.valueOf(stage + 1) + "lnweakdivall");
        ret.add(String.valueOf(stage + 1) + "lnrepostnum");
        return ret;
    }

    private static String makePredictRowKey(String source, String uid, String tid) {
        String ret = source + "e";
        ret += uid;
        ret += "_";
        ret += tid;
        return ret;
    }

    private static List<String> makePredictValues(int strong, int rep, int weakrepost, double weakdivall, double lnweakdivall, double lnrepostnum) {
        List ret = new ArrayList<String>();
        ret.add(String.valueOf(strong));
        ret.add(String.valueOf(rep));
        ret.add(String.valueOf(weakrepost));
        ret.add(String.valueOf(weakdivall));
        ret.add(String.valueOf(lnweakdivall));
        ret.add(String.valueOf(lnrepostnum));
        return ret;
    }

}
