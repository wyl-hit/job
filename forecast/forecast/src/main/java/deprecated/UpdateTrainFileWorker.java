package deprecated;

import processor.CalcWeakTieProcessor;
import processor.UpdateTrainFileProcessor;
import setting.Configs;
import util.activeMQ.Consumer;
import util.HQuery;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

/**
 * Created by wyl on 2017/2/20.
 */
public class UpdateTrainFileWorker {

    public static void main(String[] args){
        Consumer consumer = new Consumer(Configs.TrainQueue);
        try {
            //设置线程池的线程数
            ExecutorService ThreadPool = Executors.newFixedThreadPool(Configs.NTain);
            while (true) {
                for (; ((ThreadPoolExecutor) ThreadPool).getActiveCount() >= Configs.NTain;
                     Thread.sleep(Configs.MainThreadWaitTime))
                    ;
                String message = consumer.receive();
                if (null != message) {
                    //创建新线程处理当前任务
                    String[] msg = message.split(" ");//message = “resource userid”;e.g.:a 1111
//                    System.out.println(message);
                    if (msg.length < 2) {
                        continue;
                    }
                    Thread thread = new Thread(new UpdateTrainFileProcessor(msg[0], msg[1]));
                    ThreadPool.execute(thread);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            CalcWeakTieProcessor.db.close();
            HQuery.close();
            consumer.close();
        }
    }
}
