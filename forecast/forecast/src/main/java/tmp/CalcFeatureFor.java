package tmp;

import setting.Configs;
import util.DBUtil;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Created by master on 2017/2/23.
 */
public class CalcFeatureFor {
    public static final String[] sources = new String[]{
//            "a",
            "b",
//			"c",
//			"d"
    };
    public static void main(String[] args){

        for(String source : sources) {



            int count = 30;

            DBUtil db = new DBUtil(source);
            String sql = "select uid,strong_num from user order by strong_num desc";

            ExecutorService ThreadPool = Executors.newFixedThreadPool(Configs.NCalcFeature);
            List result = db.query(sql);
            for(Object m : result) {
//                if(count-- > 20){
//                    continue;
//                }
//                if(count-- < 0){
//                    break;
//                }
                Map r = (Map) m;


                for(String message : CalcFeatureSender.messages(source, r.get("uid").toString())){

                    System.out.println(message);


                    Thread thread = new Thread(new CalcFeatureProcessor(message));
                    ThreadPool.execute(thread);
                }


            }

            db.close();


        }

//                messages("1223762662");
    }
}
