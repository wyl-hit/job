package schedule;

import setting.Configs;
import util.HDFSUtil;
import java.util.List;


public class DeleteFileThread implements Runnable{
	public void run(){
		
		//@TODO filepathchange
		String filePath = Configs.predictPrefixPath;
		
		//get file list
		List<String> fileList = HDFSUtil.getHDFSFile(filePath);

		//delay 5min
		try{
			Thread.sleep(3000);
		} catch(Exception e){
			e.printStackTrace();
		}
		
		//delete file
		for(String file : fileList){
			try{
				HDFSUtil.delHDFSFile(filePath + file);
			} catch(Exception e){
				e.printStackTrace();
			}
		}
		
	}

}
