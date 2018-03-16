package RUN;

import org.apache.activemq.command.ActiveMQObjectMessage;
import processor.CalcFeatureProcessor;
import setting.Configs;
import util.activeMQ.ActiveMQUtils;
import util.HQuery;

import javax.jms.*;
import java.util.HashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

/**
 * Created by timz on 2017/2/17.
 */
public class CalcFeatureWorker {
    public static void main(String[] args) {
        //获取一条微博一个时间段的特征，可多开
        Connection conn = null;
        Session session = null;
        try {
            //MQ设置
            conn = ActiveMQUtils.getConnection();
            conn.start();
            session = conn.createSession(Boolean.FALSE, Session.AUTO_ACKNOWLEDGE);
            Destination destination = session.createQueue(Configs.FeatureQueue);
            MessageConsumer consumer = session.createConsumer(destination);

            //设置Worker线程池的线程数
            ExecutorService ThreadPool =
                    Executors.newFixedThreadPool(Configs.NCalcFeature);
            for (; ((ThreadPoolExecutor) ThreadPool).getActiveCount()
                    >= Configs.MainThreadWaitTime;
                 Thread.sleep(Configs.MainThreadWaitTime))
                ;



            while (true) {
                //此处获取对象消息
                ActiveMQObjectMessage message = (ActiveMQObjectMessage) consumer.receive();
                if (null != message) {
                    HashMap<String, String> qdata = (HashMap<String, String>) message.getObject();
//                    Thread thread = new Thread(new CalcFeatureThread(qdata.get("type")
                    Thread thread = new Thread(new CalcFeatureProcessor(qdata.get("type")
                            + " " + qdata.get("stage")
                            + " " + qdata.get("uid")
                            + " " + qdata.get("tid")
                            + " " + qdata.get("posttime")
                    ));
                    ThreadPool.execute(thread);
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            HQuery.hbaseUtil.close();
            try {
                if (null != session)
                    session.close();
                if (null != conn)
                    conn.close();
            } catch (Throwable ignore) {

            }
        }
    }
}
