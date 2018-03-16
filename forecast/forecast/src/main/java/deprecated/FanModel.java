package deprecated;

import util.*;

import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import java.sql.Timestamp;


/**
 * @author wyl
 * @time 2016-5-29
 * @description 用户粉丝模块，主要从数据库用户信息表与转发表获取用户粉丝特征
*/
public class FanModel {
	/**
	 * @param userId, hours 特征获取的时间
	 * @return null
	 * @description ，微薄发表hours时间内的点赞与分享特征
	*/
	public static HashMap<Integer, Integer> stage_time = new HashMap<Integer, Integer>(){
		{
			put(1, 3);//3h
			put(2, 6);//6h
			put(3, 12);//12h
			put(4, 24);//24h
			put(5, 72);//72h
			put(6, 168);//168h
			put(7, -1);//不限时间
		}
	};
	public static UrlUtils u =new UrlUtils();

	/**
	 * @return Map<msgid, createdTime>
	*/
	public Map<String, Timestamp> getMsgPostTime(String mid) {
		DBUtil db = new DBUtil();
		Map<String, Timestamp> msgPostTimeMap = new HashMap<String, Timestamp>();
		String sqlGetMsgId = "select post_time from weibo where id = '" + mid + "'" ;

		try{
			System.out.println("---------------");
			System.out.println(sqlGetMsgId);
			System.out.println("---------------");
			ResultSet rs = db.query1(sqlGetMsgId);
			while(null != rs && rs.next()){
//				String mid = rs.getString("mid");
//				Timestamp post_time = rs.getTimestamp("post_time");
				msgPostTimeMap.put(mid,rs.getTimestamp("post_time"));
			}
			rs.close();
		} catch(Exception e){
			System.out.println(sqlGetMsgId);
			e.printStackTrace();
		} finally {
			db.close();
		}
		return msgPostTimeMap;
	}


	/**
	 * @return Map<msgid, createdTime>
	*/
	public Map<String, Timestamp> getUserMsgPostTime(String userId) {
		DBUtil dbsql = new DBUtil();
		Map<String, Timestamp> msgPostTimeMap = new HashMap<String, Timestamp>();
		String sqlGetMsgId = "select id, post_time from weibo where uid = " + userId;

		try{
			ResultSet rs = dbsql.query1(sqlGetMsgId);
			while(null != rs && rs.next()){
//				String mid = rs.getString("mid");
//				Timestamp post_time = rs.getTimestamp("post_time");
				msgPostTimeMap.put(rs.getString("id"),rs.getTimestamp("post_time"));
			}
			rs.close();
		} catch(Exception e){
			System.out.println("*****************");
			System.out.println(sqlGetMsgId);
			System.out.println("*****************");
			e.printStackTrace();
		} finally {
			dbsql.close();
		}
		return msgPostTimeMap;
	}
	/**
	 * @return Map<msgid, <repost_usercard, repost_time, repost_likeNum, repost_reNum>>
	*/
	public List<MsgShareDetail> getUserMsgShareDetail(String msgId){
		DBUtil dbsql = new DBUtil();
//		String sqlShareDetail = "select c_uid, repost_time, like_num, repost_reNum from repost where wid = " + msgId;
		String sqlShareDetail = "select c_uid, repost_time, like_num from repost2 where wid = " + msgId;
		ResultSet rs = null;
		List<MsgShareDetail> userMsgShareDetail = new ArrayList<MsgShareDetail>();

		try{
			try{
				rs = dbsql.query1(sqlShareDetail);
				while(null != rs && rs.next()){
//					userMsgShareDetail.add(new MsgShareDetail(rs.getString("repost_usercard"), rs.getInt("repost_likeNum"), rs.getInt("repost_reNum"), rs.getTimestamp("repost_time")));
					userMsgShareDetail.add(new MsgShareDetail(rs.getString("c_uid"), rs.getInt("like_num"), rs.getTimestamp("repost_time")));
				}
				rs.close();
			} catch(Exception e){
				System.out.println("*****************");
				System.out.println(sqlShareDetail);
				System.out.println("*****************");
				e.printStackTrace();
			}
		} finally{
			dbsql.close();
		}


		return userMsgShareDetail;
	}

	/**建模特征
	*/
	public void getEachMsgFeature(String userId) throws Exception{
		WeakTie weakTie = new WeakTie();
		Map<String, Timestamp> userMsgPostTime = getUserMsgPostTime(userId);
		HDFSUtil hdfs = new HDFSUtil();

		String data = "";

		for(String msgIdtemp : userMsgPostTime.keySet()){
			String msgId = u.Uid2Mid(msgIdtemp);
			Timestamp msgPostTime = userMsgPostTime.get(msgId);
			Timestamp predictTime = msgPostTime;
			List<MsgShareDetail> userMsgShareDetail = getUserMsgShareDetail(msgId);
			List<Integer> feature = new ArrayList<Integer>();
			List<Integer> label = new ArrayList<Integer>();

			for(int i = 1; i < 6; i++){
				msgPostTime.setHours(msgPostTime.getHours() + stage_time.get(i));
				predictTime.setHours(msgPostTime.getHours() + stage_time.get(i + 1));
				long weakTieNum = weakTie.getWeakTieNum(userId, msgId, msgPostTime);


				int stage_repost_num = 0;
				int stage_like_num = 0;
				int label_repost_num = 0;

				for(MsgShareDetail msgShareDetail : userMsgShareDetail){
					if(msgShareDetail.shareTime.before(msgPostTime)){
						stage_like_num += msgShareDetail.likeCount;
						//stage_repost_num += msgShareDetail.shareCount;
						stage_repost_num += 1;
					}
					if(msgShareDetail.shareTime.before(predictTime)){
						//label_repost_num +=  msgShareDetail.shareCount;
						label_repost_num += 1;
					}
				}
				feature.add((int)weakTieNum);
				feature.add(stage_repost_num);
				feature.add(stage_like_num);
				feature.add(0);//记忆效应：设为0
				label.add(label_repost_num);
			}

			ArrayList<String> resultFeature = new ArrayList<String>();

			for(int i = 0; i < 5; i++){
				String rf = "";
				rf = rf + label.get(i) + " ";
				int j = 0;
				for(j = 0; j < (i + 1)* 4; j++){
					rf = rf + (j + 1) + ":" + feature.get(j) + " ";
				}
				for(int k = j+1; k <= 24; k++){
					rf = rf + k + ":0 ";
				}

				rf += "25:0";//影响力
				data += (rf) + "\n";
				resultFeature.add(rf);
			}

		}
		data = data.substring(0, data.length() - 1);
		hdfs.writeToHDFS("/user/root/jx/forecast/training/" + userId, data);

	}

	//timeRange: 取timeRange（年）内的微博作为特征库
	public void getEachMsgFeature(String userId, int timeRange) throws Exception{
		WeakTie weakTie = new WeakTie();
		Map<String, Timestamp> userMsgPostTime = getUserMsgPostTime(userId);
		HDFSUtil hdfs = new HDFSUtil();
		String data = "";

		Timestamp range = new Timestamp(System.currentTimeMillis());
		//range.setYear(range.getYear() - timeRange);
		range.setMonth(range.getMonth() - timeRange);
		int wnum = 0;

		for(String msgIdtemp : userMsgPostTime.keySet()){
			wnum += 1;
			String msgId = u.Uid2Mid(msgIdtemp.split("_")[2]);
			Timestamp msgPostTime = userMsgPostTime.get(msgIdtemp);
			if((null==msgPostTime) || msgPostTime.before(range)){
				continue;
			}

			System.out.println("------------------");
			System.out.println("第"+wnum+"微博");
			System.out.println(msgId);
			System.out.println(msgIdtemp);
			System.out.println(msgPostTime);
			System.out.println(range);
			System.out.println("------------------");

			Timestamp predictTime = msgPostTime;
			List<MsgShareDetail> userMsgShareDetail = getUserMsgShareDetail(msgId);
			List<Integer> feature = new ArrayList<Integer>();
			List<Integer> label = new ArrayList<Integer>();

			for(int i = 1; i < 6; i++){
				msgPostTime.setHours(msgPostTime.getHours() + stage_time.get(i));
				predictTime.setHours(msgPostTime.getHours() + stage_time.get(i + 1));
				long weakTieNum = weakTie.getWeakTieNum(userId, msgId, msgPostTime);


				int stage_repost_num = 0;
				int stage_like_num = 0;
				int label_repost_num = 0;

				for(MsgShareDetail msgShareDetail : userMsgShareDetail){
					if(msgShareDetail.shareTime.before(msgPostTime)){
						stage_like_num += msgShareDetail.likeCount;
						stage_repost_num += 1;
					}
					if(msgShareDetail.shareTime.before(predictTime)){
						label_repost_num +=  1;
					}
				}
				feature.add((int)weakTieNum);
				feature.add(stage_repost_num);
				feature.add(stage_like_num);
				feature.add(0);//记忆效应：设为0
				label.add(label_repost_num);
			}

			ArrayList<String> resultFeature = new ArrayList<String>();

			for(int i = 0; i < 5; i++){
				String rf = "";
				rf = rf + label.get(i) + " ";
				int j = 0;
				for(j = 0; j < (i + 1)* 4; j++){
					rf = rf + (j + 1) + ":" + feature.get(j) + " ";
				}
				for(int k = j+1; k <= 24; k++){
					rf = rf + k + ":0 ";
				}

				rf += "25:0";//影响力
				data += (rf) + "\n";
				resultFeature.add(rf);
			}


		}
		if(data.length()>0){
			data = data.substring(0, data.length() - 1);
			hdfs.writeToHDFS("/user/root/jx/forecast/training/" + userId, data);
		}
	}

	/**预测特征 3的时候得到stage_time.get(3)小时的特征   1 2 3 4 5
	*/
	public void getPredictFeature(String userId, String msgId, int stage) throws Exception{
		WeakTie weakTie = new WeakTie();
		//转换id
		System.out.println("in getPredictFeature");
		System.out.println(userId+" "+msgId+" " + stage);
		Map<String, Timestamp> msgPostTime = getMsgPostTime(userId+"_M_"+u.getMidbyId(msgId));
		HDFSUtil hdfs = new HDFSUtil();
		int stagep = stage + 1;
		String data = userId + "-" + msgId + "-" + stagep + "," + "0 ";
		//转换id
			Timestamp postTime = msgPostTime.get(userId+"_M_"+u.getMidbyId(msgId));

			List<MsgShareDetail> userMsgShareDetail = getUserMsgShareDetail(msgId);
			List<Integer> feature = new ArrayList<Integer>();

			for(int i = 1; i < (stage+1); i++){
				postTime.setHours(postTime.getHours() + stage_time.get(i));
				long weakTieNum = weakTie.getWeakTieNum(userId, msgId, postTime);


				int stage_repost_num = 0;
				int stage_like_num = 0;
				int label_repost_num = 0;

				for(MsgShareDetail msgShareDetail : userMsgShareDetail){
					if(msgShareDetail.shareTime.before(postTime)){
						stage_like_num += msgShareDetail.likeCount;
						stage_repost_num += 1;
					}
				}
				feature.add((int)weakTieNum);
				feature.add(stage_repost_num);
				feature.add(stage_like_num);
				feature.add(0);//记忆效应：设为0
			}

				int j = 0;
				for(j = 0; j < stage * 4; j++){
					data = data + (j + 1) + ":" + feature.get(j) + " ";
				}
				for(int k = j+1; k <= 24; k++){
					data = data + k + ":0 ";
					feature.add(0);//补零供以下用
				}

				data += "25:0";//影响力
		String writesql = "REPLACE INTO `model_predict` (" +
									"`wid`,`uid` ," +
									"`1likenum` ,`1repostnum` ,`1strong_repostnum` , `1result` ,"+
									"`2likenum` ,`2repostnum` ,`2strong_repostnum` , `2result` ,"+
									"`3likenum` ,`3repostnum` ,`3strong_repostnum` , `3result` ,"+
									"`4likenum` ,`4repostnum` ,`4strong_repostnum` , `4result` ,"+
									"`5likenum` ,`5repostnum` ,`5strong_repostnum` , `5result` ,"+
									"`6likenum` ,`6repostnum` ,`6strong_repostnum` , `6result` ) VALUES (";
		writesql = writesql + "'"+msgId+"'," + "'"+userId+"',";
		for(int i=0; i<5; i++){
			writesql = writesql + feature.get(4*i+2) + ",";
			writesql = writesql + feature.get(4*i+1) + ",";
			writesql = writesql + feature.get(4*i) + ",";
			writesql = writesql + feature.get(4*i+1) + ",";
		}
		writesql = writesql + feature.get(4*5+2) + ",";
		writesql = writesql + feature.get(4*5+1) + ",";
		writesql = writesql + feature.get(4*5) + ",";
		writesql = writesql + feature.get(4*5+1) + ")";
		DBUtil dbsql = new DBUtil();
		ResultSet rs = dbsql.query1(writesql);
		// TODO: handle exception
		System.out.println("*****************");
		System.out.println(writesql);
		System.out.println("*****************");
		dbsql.close();
		if(stage < 6)
			hdfs.writeToHDFS("/user/root/jx/forecast/predict/" + msgId+"-"+stage, data);
	}

	private static List<String> GetAllDetectUser() {
		// TODO Auto-generated method stub
		DBUtil dbsql = new DBUtil();
		String sqlGetMsgId = "select uid from user";
		System.out.println("---------------");
		System.out.println(sqlGetMsgId);
		System.out.println("---------------");
		ResultSet rs = dbsql.query1(sqlGetMsgId);
		List<String> allsuerList = new ArrayList<String>();
		try{
			while(null != rs && rs.next()){
				allsuerList.add(rs.getString("uid"));
			}
			rs.close();
		} catch(Exception e){
			e.printStackTrace();
		} finally {
			dbsql.close();
		}
		return allsuerList;
	}



	public static void main(String ...strings ) throws Exception{
		FanModel fanModel = new FanModel();
//		String userId = "5187664653";
//		String writesql = "SELECT id FROM weibo WHERE uid='" + userId + "' and post_time>'2016-08-01'";
//		DBsql dbsql = new DBsql();
//		List<String> msgidList = new ArrayList<String>();
//		try{
//			try{
//				ResultSet rs = dbsql.query(writesql);
//				while(null != rs && rs.next()){
////					userMsgShareDetail.add(new MsgShareDetail(rs.getString("repost_usercard"), rs.getInt("repost_likeNum"), rs.getInt("repost_reNum"), rs.getTimestamp("repost_time")));
//					msgidList.add(rs.getString("id"));
//				}
//				rs.close();
//			} catch(Exception e){
//				System.out.println("*****************");
//				System.out.println(writesql);
//				System.out.println("*****************");
//				e.printStackTrace();
//			}
//		} finally{
//			dbsql.close();
//		}
		//List<String> userList = GetAllDetectUser();
		//for(String userId:userList){
		//	if(Integer.parseInt(userId) >= Integer.parseInt("1296241304"))
		fanModel.getEachMsgFeature("1746274673", 12);
		//}
//		for(String msgid : msgidList)
//			for(int i=1; i<=6; i++)
//				fanModel.getPredictFeature(userId, u.Uid2Mid(msgid.split("_")[2]), i);
//		System.out.println("\n");
	}



}

