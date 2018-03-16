package schedule;

import deprecated.UpdateTrainFileSender;


/**
 * Created by dapt on 2017/2/17.
 */


//CalcFeatureProcessor

public class UpdateTrainFileThread implements Runnable {

    public static final String[] sources = new String[]{
            "a",
            "b",
//            "c",
//            "d"
    };


    public static void main(String[] args){

    }

    public void run(){
        for(String source : sources) {
             UpdateTrainFileSender.sender(source);
        }
    }
}
