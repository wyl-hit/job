package tmp;

import setting.Configs;
import util.activeMQ.Consumer;
import util.HQuery;
import util.HbaseUtil;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

/**
 * Created by timz on 2017/2/17.
 */
public class CalcFeatureWorker {
    public static HbaseUtil dbpredict = new HbaseUtil()
            .table(Configs.tableName)
            .family(Configs.familyPredict);//write to predict

    public static void main(String[] args) {
        //获取一条微博一个时间段的特征，可多开

        Consumer consumer = new Consumer("tmp_Forecast_CalcFeatureQ");
        try {
            //设置线程池的线程数
            ExecutorService ThreadPool = Executors.newFixedThreadPool(Configs.NCalcFeature);
            while (true) {
                for (; ((ThreadPoolExecutor) ThreadPool).getActiveCount() >= Configs.NCalcFeature;
                     Thread.sleep(Configs.MainThreadWaitTime))
                    ;

                String message = consumer.receive();
                if (null != message) {
//                    HashMap<String, String> qdata = (HashMap<String, String>) message.getObject();
//                    Thread thread = new Thread(new CalcFeatureThread(qdata.get("type")
//                    Thread thread = new Thread(new CalcFeatureProcessor(message));
//                    ThreadPool.execute(thread);
                    System.out.println(message);
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            dbpredict.close();
            HQuery.hbaseUtil.close();
            consumer.close();

        }
    }
}
