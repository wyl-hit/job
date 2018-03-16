package sparkJob.forecast;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.URI;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Properties;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.DataFrame;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SQLContext;

import bsh.This;

public class WriteFromMysql {
	private static  String MYSQL_CONNECTION_URL = "jdbc:mysql://192.168.18.206:3306/forecast";
	private static  String MYSQL_USERNAME = "root";
	private static  String MYSQL_PWD = "123456";
	public static void main(String[] args){
		testwritefile(args[0]);
	}
	public static void testwritefile(String timeString) {
		// TODO Auto-generated method stub
		SparkConf conf = new SparkConf().setAppName("readmysqlDF").set("spark.kryoserializer.buffer.max","1g");
		JavaSparkContext sc = new JavaSparkContext(conf);
		SQLContext sqlContext = new SQLContext(sc);
		String textpath = "/user/root/jx/classify/streamingtemp/";
		String table = "weibo";
		// 读取条件
		//String[] predicates = new String[] {"uid='1003061305787691'"};
		Date date;
		Calendar cal;
		String timeString2 = "2012-12-01";
		try {
			date = (new SimpleDateFormat("yyyy-MM-dd")).parse(timeString);
			cal = Calendar.getInstance();
			cal.setTime(date);
			cal.add(Calendar.MONTH, 1);
			timeString2 = (new SimpleDateFormat("yyyy-MM-dd")).format(cal.getTime());
		} catch (ParseException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}
		int file_num = 0;
//		while(!timeString.equals("2017-02-01")){
//		String[] predicates = new String[] {"post_time>='"+timeString+"' and post_time<'"+timeString2+"'"};
		String[] predicates = new String[] {"type is Null"};
		try {
			date = (new SimpleDateFormat("yyyy-MM-dd")).parse(timeString2);
			timeString = timeString2;
			cal = Calendar.getInstance();
			cal.setTime(date);
			cal.add(Calendar.MONTH, 1);
			timeString2 = (new SimpleDateFormat("yyyy-MM-dd")).format(cal.getTime());
		} catch (ParseException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		System.out.println(timeString+"\t"+timeString2);
		Properties connectionProperties = new Properties();
		connectionProperties.setProperty("dbtable", table);
		connectionProperties.setProperty("user", MYSQL_USERNAME);
		connectionProperties.setProperty("password", MYSQL_PWD);
		//也可以加读取条件
		DataFrame jbdcDataFrame = sqlContext.read().jdbc(MYSQL_CONNECTION_URL, table, predicates, connectionProperties).select("id", "content");
		jbdcDataFrame.show(10);
		
		Configuration confhdfs = new Configuration();
		
		Path path = null;
		BufferedWriter out = null;
		FileSystem fs = null;
		FSDataOutputStream fout = null;
		try{
			fs = FileSystem.get(URI.create(textpath + "test"+file_num),confhdfs);
			path = new Path(textpath + "test" + file_num);
			fout = fs.create(path);
			out = new BufferedWriter(new OutputStreamWriter(fout,"UTF-8"));
			int tempk = 0;
			for(Row tempRow:jbdcDataFrame.collect()){
				tempk++;
				if(tempk > 500){
//					break;
					tempk = 0;
					try {
						Thread.sleep(5000);
					} catch (InterruptedException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					out.flush();
					try {
						out.close();
					} catch (IOException e) {
						e.printStackTrace();
					}
					fs.rename(path, new Path("/user/root/jx/classify/streamingtext/test"+file_num));
					file_num++;
					fs = FileSystem.get(URI.create(textpath + "test"+file_num),confhdfs);
					path = new Path(textpath + "test" + file_num);
					fout = fs.create(path);
					out = new BufferedWriter(new OutputStreamWriter(fout,"UTF-8"));
				}
				out.write(tempRow.getString(0)+"\t"+tempRow.getString(1)+"\n");
			}
			out.flush();
			fs.rename(path, new Path("/user/root/jx/classify/streamingtext/test"+file_num));
		}catch (IOException e) {
			// TODO: handle exception
			e.printStackTrace();
		}finally{
			try {
				out.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
//		}
		
	}
	public static void Hbasewritefile() {
		// TODO Auto-generated method stub
		SparkConf conf = new SparkConf().setAppName("readmysqlDF");
		JavaSparkContext sc = new JavaSparkContext(conf);
		SQLContext sqlContext = new SQLContext(sc);
		String textpath = "/user/root/jx/classify/streamingtemp/";
		String table = "weibo";
		// 读取条件
		//String[] predicates = new String[] {"uid='1003061305787691'"};
		String[] predicates = new String[] {"1=1"};
		Properties connectionProperties = new Properties();
		connectionProperties.setProperty("dbtable", table);
		connectionProperties.setProperty("user", MYSQL_USERNAME);
		connectionProperties.setProperty("password", MYSQL_PWD);
		//也可以加读取条件
		DataFrame jbdcDataFrame = sqlContext.read().jdbc(MYSQL_CONNECTION_URL, table, predicates, connectionProperties).select("mid", "content");
		jbdcDataFrame.show(10);
		
		Configuration confhdfs = new Configuration();
		
		Path path = null;
		BufferedWriter out = null;
		FileSystem fs = null;
		FSDataOutputStream fout = null;
		try{
			int file_num = 0;
			fs = FileSystem.get(URI.create(textpath + "test"+file_num),confhdfs);
			path = new Path(textpath + "test" + file_num);
			fout = fs.create(path);
			out = new BufferedWriter(new OutputStreamWriter(fout,"UTF-8"));
			int tempk = 0;
			for(Row tempRow:jbdcDataFrame.collect()){
				tempk++;
				if(tempk > 500){
//					break;
					tempk = 0;
					try {
						Thread.sleep(5000);
					} catch (InterruptedException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					out.flush();
					try {
						out.close();
					} catch (IOException e) {
						e.printStackTrace();
					}
					fs.rename(path, new Path("/user/root/jx/classify/streamingtext/test"+file_num));
					file_num++;
					fs = FileSystem.get(URI.create(textpath + "test"+file_num),confhdfs);
					path = new Path(textpath + "test" + file_num);
					fout = fs.create(path);
					out = new BufferedWriter(new OutputStreamWriter(fout,"UTF-8"));
				}
				out.write(tempRow.getString(0)+"\t"+tempRow.getString(1)+"\n");
			}
			out.flush();
			fs.rename(path, new Path("/user/root/jx/classify/streamingtext/test"+file_num));
		}catch (IOException e) {
			// TODO: handle exception
			e.printStackTrace();
		}finally{
			try {
				out.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		
		
	}
}
