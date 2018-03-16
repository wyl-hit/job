package RUN;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

import setting.Configs;
import util.activeMQ.Consumer;
import processor.FeaturePredictProcessor;



//预测任务由爬虫发送

public class DetectPredictWorker {
    public static void main(String[] args){
        Consumer consumer = new Consumer(Configs.PredictQueue);
        try {
            //设置线程池的线程数

            ExecutorService ThreadPool = Executors.newFixedThreadPool(Configs.NDetectPredict);

            while (true) {
                for (; ((ThreadPoolExecutor) ThreadPool).getActiveCount() >= Configs.NDetectPredict;
                     Thread.sleep(Configs.MainThreadWaitTime)) {}


                String message = consumer.receive();
                if (null != message) {
                    //创建新线程处理当前任务
                    String[] task = message.split(" ");
                    String source = task[0];
                    String uid = task[1];
                    String msgid = task[2];
                    int stage = Integer.parseInt(task[3]);

                    Thread thread = new Thread(new FeaturePredictProcessor(source, uid, msgid, stage));
                    ThreadPool.execute(thread);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            consumer.close();
        }
    }
}
