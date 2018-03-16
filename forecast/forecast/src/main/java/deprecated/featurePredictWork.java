package deprecated;

public class featurePredictWork implements Runnable{
	
	String userId = null;
	String msgId = null;
	FanModel fanModel = null;
	int Stage = 0;
	public featurePredictWork(String userid, String msgid, int stage){
		fanModel = new FanModel();
		userId = userid;
		msgId = msgid;
		Stage = stage;
	}

	@Override
	public void run() {
		// TODO Auto-generated method stub
		try {
			fanModel.getPredictFeature(userId, msgId, Stage);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
