package schedule;

import java.io.IOException;

//定时提交建模任务
public class TrainThread implements Runnable{
	public void run(){
		Process process = null;
		// TODO 建模程序jar包地址
        String cmd = "spark-submit --class sparkJob.forecast.ForecastBuildModel /usr/local/jx/forecastBuildModel.jar";
		Runtime rt = Runtime.getRuntime();
        try {
            process = rt.exec(cmd);
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        try {
            process.waitFor();
        } catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        
        
        
        
	}
}
