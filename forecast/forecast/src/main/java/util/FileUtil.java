package util;

/**
 * <p>Title:FileUtil</p>
 * <p>Description:文件读写工具类</P>
 * @author:wyl
 * @date:2016年10月4日 下午7:21:46
 */

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
public class FileUtil {
	public static String read(String filePath){
		File file = new File(filePath);
		String result = "";
		try {
			BufferedReader br = new BufferedReader(new FileReader(file));
			String temp = null;
			try {
				while((temp = br.readLine()) != null)
					result += temp;
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return result;
	}
	
	public static void write(String filePath, String data){
		File file = new File(filePath);
		try{
			if(!file.exists()){
				file.createNewFile();
			}
			FileWriter fileWriter = new FileWriter(filePath);
			BufferedWriter bufferWriter = new BufferedWriter(fileWriter);
			bufferWriter.write(data);
			bufferWriter.close();
			fileWriter.close();
		} catch(IOException e){
			e.printStackTrace();
		} finally{
		}
	}
	
	public static void main(String[] args){
//		System.out.println(read("E:\\1.json"));
		
	}
}
