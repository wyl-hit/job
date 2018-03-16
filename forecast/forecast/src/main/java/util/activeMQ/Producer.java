package util.activeMQ;

import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.DeliveryMode;
import javax.jms.Destination;
import javax.jms.MessageProducer;
import javax.jms.Session;
import javax.jms.TextMessage;
import org.apache.activemq.ActiveMQConnection;
import org.apache.activemq.ActiveMQConnectionFactory;

public class Producer {

	//ConnectionFactory ：连接工厂，JMS 用它创建连接
    ConnectionFactory connectionFactory;
    // Connection ：JMS 客户端到JMS Provider 的连接
    Connection connection = null;
    // Session： 一个发送或接收消息的线程
    Session session;
    // Destination ：消息的目的地;消息发送给谁.
    Destination destination;
    // MessageProducer：消息发送者
    MessageProducer producer;
    // TextMessage message;
    // 构造ConnectionFactory实例对象，此处采用ActiveMq的实现jar
    
    public Producer(String queueName){
    	try{
    		connectionFactory = new ActiveMQConnectionFactory(
                ActiveMQConnection.DEFAULT_USER,
                ActiveMQConnection.DEFAULT_PASSWORD,
                "tcp://192.168.18.207:61616");
    		// 构造从工厂得到连接对象
    		this.connection = connectionFactory.createConnection();
    		// 启动
    		this.connection.start();
    		// 获取操作连接
    		this.session = connection.createSession(Boolean.TRUE,Session.AUTO_ACKNOWLEDGE);
    		// 获取session注意参数值xingbo.xu-queue是一个服务器的queue，须在在ActiveMq的console配置
    		this.destination = session.createQueue(queueName);
    		// 得到消息生成者【发送者】
    		this.producer = session.createProducer(destination);
    		// 设置不持久化，此处学习，实际根据项目决定
    		this.producer.setDeliveryMode(DeliveryMode.PERSISTENT);
    		// 构造消息，此处写死，项目就是参数，或者方法获取
        } catch (Exception e) {
            e.printStackTrace();
        } 
    }
    
	public void close(){
		if (null != this.connection){
			try {
                this.connection.close();
			} catch (Throwable ignore) {
			}
		}
	}
    
    
    public void sendMessage(String message) {
    	try{
    		TextMessage Text = this.session.createTextMessage(message);
    		this.producer.send(Text);
    		this.session.commit();
    	} catch(Exception e){
    		e.printStackTrace();
    	} 
    }
    
//    接收者无法实现MapMessage的遍历
//    public void sendMessage(Map<String, String> message) {
//    	try{
//        	MapMessage mapMessage = session.createMapMessage();
//    		for(String key : message.keySet()){
//    			mapMessage.setString(key, message.get(key));
//    		}
//    		producer.send(mapMessage);
//    		session.commit();
//    	} catch(Exception e){
//    		e.printStackTrace();
//    	} 
//    }

	public static void main(String[] args){
		Producer producer = new Producer("producer");
		producer.sendMessage("producer");
		producer.close();
	}

    
}