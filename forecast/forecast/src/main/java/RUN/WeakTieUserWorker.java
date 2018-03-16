package RUN;

import processor.CalcWeakTieProcessor;
import setting.Configs;
import util.activeMQ.Consumer;
import util.HQuery;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

/**
 * Created by d3 on 2017/2/17.
 */
public class WeakTieUserWorker {
    public static void main(String[] args) {
        Consumer consumer = new Consumer(Configs.WeaktieQueue);
        try {
            //设置线程池的线程数
            ExecutorService ThreadPool = Executors.newFixedThreadPool(Configs.NWeakTie);
            while (true) {
                for (; ((ThreadPoolExecutor) ThreadPool).getActiveCount() >= Configs.NWeakTie;
                     Thread.sleep(Configs.MainThreadWaitTime))
                    ;
                String message = consumer.receive();
                if (null != message) {
                    //创建新线程处理当前任务
                    //message = “resource userid”;e.g.:a 1111
                    String[] msg = message.split(" ");
                    System.out.println(message);
                    if (msg.length < 2) {
                        continue;
                    }
                    Thread thread = new Thread(new CalcWeakTieProcessor(msg[0], msg[1]));
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
