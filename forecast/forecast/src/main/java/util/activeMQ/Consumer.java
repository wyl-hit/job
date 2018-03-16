package util.activeMQ;

import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.MessageConsumer;
import javax.jms.Session;
import javax.jms.TextMessage;

import org.apache.activemq.ActiveMQConnection;
import org.apache.activemq.ActiveMQConnectionFactory;
import util.HbaseUtil;

import java.util.Arrays;
import java.util.HashMap;

public class Consumer {
	// ConnectionFactory ：连接工厂，JMS 用它创建连接
    ConnectionFactory connectionFactory;
    // Connection ：JMS 客户端到JMS Provider 的连接
    Connection connection = null;
    // Session： 一个发送或接收消息的线程
    Session session;
    // Destination ：消息的目的地;消息发送给谁.
    Destination destination;
    // 消费者，消息接收者
    MessageConsumer consumer;
    public static void main(String args[]) throws JMSException{
//        Consumer consumer = new Consumer("Forecast_PredictQ");
//        String message = null;
//        try {
//            while (true) {
//                message = consumer.receive();
//                if (message != null) {
//                }
//            }
//        } catch (Exception e){
//            e.printStackTrace();
//        } finally {
//            consumer.close();
//        }

//    	while(true){
//    		Consumer consumerW = new Consumer("A");
//    		HashMap<?,?> weibo_preMap=(HashMap<?,?>) consumerW.consumer.receive();
//    		featurePredictWork UserDetectionRunnable =new featurePredictWork(weibo_preMap.get("uid").toString(), weibo_preMap.get("wid").toString(), Integer.parseInt(weibo_preMap.get("stage").toString()));
//    		Thread ScheduleTaskThread =new Thread(UserDetectionRunnable);
//    	}


        HbaseUtil hbase = new HbaseUtil()
                .table("forecast")
                .family("predict");

        hbase.replaceInsert("forecast","predict","be735314581_834035354076381184", Arrays.asList(7 + "predict"),
                Arrays.asList(String.valueOf(12)));

    }
    public Consumer(String queueName){
    	connectionFactory = new ActiveMQConnectionFactory(
                ActiveMQConnection.DEFAULT_USER,
                ActiveMQConnection.DEFAULT_PASSWORD,
                "tcp://192.168.18.207:61616");
    	try{
    	    // 构造从工厂得到连接对象
            connection = connectionFactory.createConnection();
            // 启动
            connection.start();
            // 获取操作连接
            session = connection.createSession(Boolean.FALSE, Session.AUTO_ACKNOWLEDGE);
            // 获取session注意参数值xingbo.xu-queue是一个服务器的queue，须在在ActiveMq的console配置
            destination = session.createQueue(queueName);
            consumer = session.createConsumer(destination);
        
    	} catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    public void close(){
    	if (null != connection)
    		try {
                connection.close();
    		} catch (Throwable ignore) {
    		}
    }
    
	public String receive(){
		String message = null;
		TextMessage textMessage = null;
		try{
			textMessage = (TextMessage) consumer.receive();
			if(null != textMessage){
				message = textMessage.getText().toString();
			}
		} catch(Exception e){
			e.printStackTrace();
		}
		return message;
	}
    
//	MapMessage 无法遍历Key
//	public Map<String, String> recieve(){
//		Map<String, String> message = new HashMap<String, String>();
//		MapMessage mapMessage = null;
//		try{
//			mapMessage = (MapMessage) consumer.receive();
//			mapMessage.get
//		} catch(Exception e){
//			e.printStackTrace();
//		}
//		return mapMessage;
//
//	}




}