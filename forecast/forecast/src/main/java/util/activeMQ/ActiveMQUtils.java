/**
 * @Project:WebCrawler
 * @Title:MQPooledConnectionFactory.java
 * @Description:TODO
 * @autor:wing
 * @date: @2016-5-19上午10:56:38
 * @Copyright:2016 hit. All rights reserved.
 * @version:V1.0
 */
package util.activeMQ;

//import com.crawler.sinacrawler.utils.PropertyHandle;
import org.apache.activemq.ActiveMQConnection;
import org.apache.activemq.ActiveMQConnectionFactory;
import org.apache.activemq.pool.PooledConnectionFactory;

import javax.jms.*;
import java.util.Properties;

/**
 * @ClassName MQPooledConnectionFactory
 * @Description activeMQ连接工厂
 * @author wing
 * @date 2016-5-19上午10:56:38
 */
public class ActiveMQUtils {
	private static ActiveMQConnectionFactory connectionFactory; 
    // Connection ：JMS 客户端到JMS Provider 的连接
	private static Connection connection = null;
    // Session： 一个发送或接收消息的线程
	private static Session session;
    // Destination ：消息的目的地;消息发送给谁.
	private static Destination destination;
    // MessageProducer：消息发送者
	private static  MessageProducer producer;
//    public static Properties prop = PropertyHandle.getProperties();
	//获得连接工厂
	public static ActiveMQConnectionFactory getMyActiveMQConnectionFactory() {
//        String activemq = prop.getProperty("ActiveMQ");
		String activemq = "192.168.18.207:61616";
        if (null == connectionFactory) {  
            connectionFactory = new ActiveMQConnectionFactory(
            		ActiveMQConnection.DEFAULT_USER,
                    ActiveMQConnection.DEFAULT_PASSWORD,
                    "tcp://"+activemq+"?wireFormat.maxInactivityDuration=0");
        }  
        return connectionFactory;  
    } 
	
	
	
	
	

	private static PooledConnectionFactory pooledConnectionFactory; 
	
	//初始化连接池
	static{  
        try {  

            pooledConnectionFactory = new PooledConnectionFactory(getMyActiveMQConnectionFactory());  
          
            //设置最大连接数
            pooledConnectionFactory.setMaxConnections(1000);
        } catch (Exception e) {  
            e.printStackTrace();  
        }  
    }  
    
    /** 
     * 获得链接池工厂 
     */  
    public static PooledConnectionFactory getPooledConnectionFactory() {  
        return pooledConnectionFactory;  
    }
    
    
    
    //获取普通连接
    public static Connection getConnection() throws JMSException{
    	
    	return connectionFactory.createConnection();
    }
    //获取连接池连接
    public static Connection getPoolConnection() throws JMSException{
    	
    	return pooledConnectionFactory.createConnection();
    }

    /** 
     * 对象回收销毁时停止链接 
     */  
    @Override  
    protected void finalize() throws Throwable {  
        pooledConnectionFactory.stop();  
        super.finalize();  
    }  
	
	
	
}
