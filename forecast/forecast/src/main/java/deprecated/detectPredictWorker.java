package deprecated;

import org.apache.activemq.command.ActiveMQObjectMessage;
import util.activeMQ.ActiveMQUtils;

import javax.jms.*;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;


public class detectPredictWorker {
	private static Connection connection = null;
    private static Session session;
    private static Destination destination;
    private static MessageProducer producer;
    private static MessageConsumer consumer;
    private static LinkedList<String> contentList=new LinkedList<String>();
    public static int thread_num = 3;
    public static void main(String args[]) throws JMSException{
        System.setProperty("org.apache.activemq.SERIALIZABLE_PACKAGES","*");
        try {
            connection = ActiveMQUtils.getConnection();
            connection.start();
            session = connection.createSession(Boolean.FALSE, Session.AUTO_ACKNOWLEDGE);
            Destination destination = session.createQueue("B");
            consumer = session.createConsumer(destination);
            ExecutorService pool = Executors.newFixedThreadPool(thread_num);
            System.out.println("ok");
            while (true) {
                Thread.sleep(2000);
                System.out.println("ok1");
                ActiveMQObjectMessage message =(ActiveMQObjectMessage)consumer.receive(0);
                System.out.println("ok2");
                if (null != message) {
                	HashMap<String,String> weibo_preMap=(HashMap<String,String>) message.getObject();
                	System.out.println("---------------------");
                    featurePredictWork UserDetectionRunnable =new featurePredictWork(weibo_preMap.get("uid"), weibo_preMap.get("wid"), Integer.parseInt(weibo_preMap.get("stage")));
                    System.out.println(weibo_preMap.get("uid")+" "+weibo_preMap.get("wid")+" "+Integer.parseInt(weibo_preMap.get("stage")));
                    Thread ScheduleTaskThread =new Thread(UserDetectionRunnable);
                    pool.execute(ScheduleTaskThread);
                    int threadCount = ((ThreadPoolExecutor)pool).getActiveCount();
                    while(threadCount == thread_num){
                        Thread.sleep(3*1000);
                        threadCount = ((ThreadPoolExecutor)pool).getActiveCount();
                    }
                } else {
                    break;
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (null != connection)
                    connection.close();
            } catch (Throwable ignore) {
            }
        }
    }
}
