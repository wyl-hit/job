package schedule;

/** 
 *  @Project: forecast
 *	@Title: Schedule.java
 *	@Author: wyl
 *  @Date: Dec 26, 2016 3:58:31 PM
 * 	@Description: TODO
 *  @Version: v1.0
 */

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class Schedule {
//	定时计算弱连接特征
//	定时清理文件
//	定时调度更新建模
//	定时计算特征并写入特征文件
//	
	
	private static ScheduledExecutorService executor = Executors.newScheduledThreadPool(10);
	
	public static void updateWeaktieFan(int n) {

        executor.scheduleAtFixedRate(
                new WeakTieThread(),
                0,
                n,
                TimeUnit.DAYS);
    }
	
	public static void deleteStreamingFile(int n){
		executor.scheduleAtFixedRate(
				new DeleteFileThread(),
				n,
				n,
				TimeUnit.DAYS);
	}
	public static void forecastBuildModel(int n){
		executor.scheduleAtFixedRate(
				new TrainThread(), 
				0,
				n,
				TimeUnit.DAYS);
	}
	
//	public static void calFeature(int n){
//		executor.scheduleAtFixedRate(
//				new CalcFeatureThread(),
//				0,
//				n,
//				TimeUnit.DAYS);
//	}

	public static void updateTrainFile(int n){
		executor.scheduleAtFixedRate(
				new UpdateTrainFileThread(),
				0,
				n,
				TimeUnit.DAYS
		);
	}
	
	
	public static void main(String[] args){
        // 每隔11天计算所有用户的强弱连接
		updateWeaktieFan(11);
		// 每隔30天清理预测任务的特征文件
		deleteStreamingFile(30);
		// 每隔17天更新训练文件
		updateTrainFile(17);
		// 每隔19天重新建立预测模型
		forecastBuildModel(19);


		// 每隔17天重新计算特征
		//特征计算由延迟队列控制
//		calFeature(17);

	}
	
}
