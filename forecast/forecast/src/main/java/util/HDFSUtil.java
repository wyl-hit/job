package util;

import java.io.BufferedReader;
import java.net.URI;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

import setting.Configs;

public class HDFSUtil {
	
	
	public static Configuration conf = new Configuration();
	public static String rootPath = Configs.hadoopConfig.get("hdfshost");
	
	

	public HDFSUtil(){
		conf.set("fs.hdfs.impl","org.apache.hadoop.hdfs.DistributedFileSystem");

//		conf.addResource(new Path("/usr/local/hadoop/etc/hadoop/core-site.xml"));
//		conf.addResource(new Path("/usr/local/hadoop/etc/hadoop/hdfs-site.xml"));
	}
	

	public static void main(String[] args) throws Exception{
		conf.set("fs.hdfs.impl","org.apache.hadoop.hdfs.DistributedFileSystem");
		writeToHDFS("/user/root/jx/forecast/" + String.valueOf(System.currentTimeMillis()) + ".data", "123456");

//		String result = readFromHDFS("/user/root/jx/forecast/1487765034517.data");
//		System.out.println(result);

//		List<String> fileList = getHDFSFile("/user/root/jx/forecast");
//		for(String file : fileList)
//					System.out.println(file);


//		createFileOnHDFS("/user/root/jx/forecast/l.txt");


//		uploadFile("D:\\data\\data.txt","/user/root/jx/forecast/data.txt");

	}
	
	
	
	/**
	 * 读取HDFS文件
	 * **/
	public static String readFromHDFS(String fileName) throws Exception{
		//读取HDFS上的文件系统
	    FileSystem fs = FileSystem.get(URI.create(rootPath + fileName),conf);
		//流读入和写入
    	InputStream in=null;
		//使用缓冲流，进行按行读取的功能
        BufferedReader buff=null;
        
        Path path = new Path(rootPath + fileName);
	    //打开读文件流
		in=fs.open(path);
   	 	//BufferedReader包装一个流
   	   	buff=new BufferedReader(new InputStreamReader(in));	       	 
   	   	String str = "";
   	   	String temp = "";
   	   	while((temp = buff.readLine())!=null){
   	   		str += temp + '\n';
        }
       	buff.close();
       	in.close();
       	fs.close();
       	return str;
	}
		
	
	/*
	读取文件系统下所有文件名
	 */
	public static List<String> getHDFSFile(String path){
		ArrayList<String> fileNameList = new ArrayList<String>();
		try {
			FileSystem hdfs = FileSystem.get(URI.create(rootPath + path), conf);
			Path listf = new Path(rootPath + path);
			FileStatus stats[] = hdfs.listStatus(listf);
			if (stats.length != 0) {
				for (FileStatus file : stats) {
					fileNameList.add(file.getPath().getName().toString());
				}
			}
			hdfs.close();
		} catch(Exception e){
			e.printStackTrace();
		}
		return fileNameList;
	}
	/* 
	 * 读取文件二级子目录名
	*/
	
	
	/**
	 *  写入HDFS文件
	 * **/
	public static void writeToHDFS(String fileName, String data) throws Exception{
		FileSystem fs = FileSystem.get(URI.create(rootPath + fileName),conf);
		
		Path path = new Path(rootPath + fileName);	

		fs = path.getFileSystem(conf);
		FSDataOutputStream fout = fs.create(path);
		BufferedWriter out = null;
		out = new BufferedWriter(new OutputStreamWriter(fout,"UTF-8"));
		out.write(data);
		out.flush();
		fs.close();
		out.close();
	}


	public static void writeHDFS(String fileName, String data) throws Exception{

	}


	
	 /***
		 * 上传本地文件到
		 * HDFS上
		 * 
		 * **/
		public static void uploadFile(String fileName, String dstFile)throws Exception{
			//加载默认配置
			FileSystem fs = FileSystem.get(URI.create(rootPath + dstFile),conf);
			//本地文件
	        Path src =new Path(fileName);
	        //HDFS为止
	        
	        Path dst =new Path(rootPath + dstFile);
	        
	        try {
	        	if(fs.exists(dst))
	        		delHDFSFile(dstFile);
				fs.copyFromLocalFile(src, dst);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	        System.out.println("上传成功........");
	   
	        fs.close();//释放资源
	 
		}
		
	
	
	/**
	 *  在HDFS上创建一个文件
	 * **/
	 public static void createFileOnHDFS(String fileName)throws Exception{
		 FileSystem fs = FileSystem.get(URI.create(rootPath + fileName),conf);
		 Path path =new Path(rootPath + fileName);
		 fs.createNewFile(path);
		 fs.close();//释放资源
	 }

	 /**
	  * 删除HDFS上的一个文件
	  * **/
	  public static void delHDFSFile(String fileName)throws Exception{
		 FileSystem fs = FileSystem.get(URI.create(rootPath + fileName),conf);
		 Path path =new Path(rootPath + fileName);
		 fs.deleteOnExit(path);
		 fs.close();//释放资源
	  }
	  
	 
	 
}
