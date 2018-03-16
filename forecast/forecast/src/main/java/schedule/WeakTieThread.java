package schedule;

import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import RUN.WeakTieUserSender;


public class WeakTieThread implements Runnable{


	public static final String[] sources = new String[]{
			"a",
			"b",
//			"c",
//			"d"
	};

	public void run(){
		for(String source : sources) {
			WeakTieUserSender.sender(source);
		}
	}


	public static void main(String... args){
	}
	
	
}




