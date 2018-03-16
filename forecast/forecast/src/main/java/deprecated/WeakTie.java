package deprecated;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;		
import java.sql.Timestamp;

import setting.Configs;
import util.DBUtil;


/**
 *  @Project: forecast
 *	@Title: WeakTie.java
 *	@Author: wyl
 *  @Date: Dec 21, 2016 5:16:09 PM
 * 	@Description: TODO
 *  @Version: v1.0
 */
public class WeakTie {

	/** 
	 * 所有粉丝，热粉标记为true，非热粉标记为false
	*/
	public static Map<String, Boolean> getWeaktieFan(String userId){
		DBUtil db = new DBUtil();
//		String sqlGetAllShareMid = "select repost_usercard, mid from repost where fromid = " + userId;
		int strongtieNum = Configs.getStrongTieNum();
		Map<String, Long> fanShareCountMap = new HashMap<String, Long>();
		Map<String, Boolean> fanMap = new HashMap<String, Boolean>();
		String sqlGetFanShareCount = "select repost_usercard, count(*) as shareNum from repost where fromId = ? GROUP BY repost_usercard";
		List<String> parameters = new ArrayList<String>();
		parameters.add(userId);
		
		List result = null;
		result = db.query(sqlGetFanShareCount, parameters);
		for(Object R : result){
			fanShareCountMap.put(((Map<String, String>)R).get("repost_usercard"), ((Map<String, Long>)R).get("shareNum"));
		}
		
		for(String shareId : fanShareCountMap.keySet()){
			if(fanShareCountMap.get(shareId) >= strongtieNum)
				fanMap.put(shareId, true);
			else
				fanMap.put(shareId, false);
		}
		db.close();
		return fanMap;
	}
	
	/** 
	 * 一段时间内的粉丝，热粉标记为true，非热粉标记为false
	 * 此前时间向前推三个月时间后传入after；
	 * @example：
	 *	Timestamp t = new Timestamp(System.currentTimeMillis());
	 *	t.setMonth(t.getMonth() - 4);
	 *	getWeaktieFan("1005051740577714", t); 
	*/
	public static Map<String, Boolean> getWeaktieFan(String userId, Timestamp after){
		DBUtil db = new DBUtil();
		int strongtieNum = Configs.getStrongTieNum();
		Map<String, Long> fanShareCountMap = new HashMap<String, Long>();
		Map<String, Boolean> fanMap = new HashMap<String, Boolean>();
		String sqlGetFanShareCount = "select c_uid, count(*) as shareNum from repost2 where from_uid = ? and repost_time > ? GROUP BY c_uid";
//		Object[] parameters = {userId, after};
		List<String> parameters = new ArrayList<String>();
		parameters.add(userId);
		parameters.add(after.toString());
		
		List result = null;
		
		result = db.query(sqlGetFanShareCount, parameters);
		for(Object R : result){
			fanShareCountMap.put(((Map<String, String>)R).get("c_uid"), ((Map<String, Long>)R).get("shareNum"));
		}
		
		for(String shareId : fanShareCountMap.keySet()){
			if(fanShareCountMap.get(shareId) >= strongtieNum){
				fanMap.put(shareId, true);
//				System.out.println(shareId);
			}
			else
				fanMap.put(shareId, false);
		}
		db.close();
		return fanMap;
	}
	
	public static List<String> repostUsercard(String mId){
		DBUtil db = new DBUtil();
		String usercardSql = "select c_uid from repost where wid = ?";
		List<String> parameters = new ArrayList<String>();
		parameters.add(mId);
		List result = db.query(usercardSql, parameters);
		List<String> usercard = new ArrayList<String>();
		for(Object R: result){
			usercard.add(((Map<String, String>)R).get("c_uid"));
		}
		db.close();
		return usercard;
	}
	
	public static List<String> repostUsercard(String mId, Timestamp after){
		DBUtil db = new DBUtil();
		String usercardSql = "select c_uid from repost2 where wid = ? and repost_time < ? ";
		List<String> parameters = new ArrayList<String>();
		parameters.add(mId);
		parameters.add(after.toString());
		List result = db.query(usercardSql, parameters);
		List<String> usercard = new ArrayList<String>();
		for(Object R: result){
			usercard.add(((Map<String, String>)R).get("c_uid"));
		}
		db.close();
		return usercard;
	}
	
	/**
	 * 获取一条微博的弱链接粉丝数
	*/
	public static Long getWeakTieNum(String userId, String mId){
		Map<String, Boolean> fanMap  = new HashMap<String, Boolean>();
		fanMap = getWeaktieFan(userId);
		List<String> usercard = repostUsercard(mId);
		Long count = new Long(0);
		for(String u : usercard){
			if(fanMap.containsKey(u) && fanMap.get(u)){
				continue;
			}
				count += 1;
		}
		return count;
	}
	
	public static Long getWeakTieNum(String userId, String mId, Timestamp after){
		Map<String, Boolean> fanMap  = new HashMap<String, Boolean>();
		fanMap = getWeaktieFan(userId, after);
		List<String> usercard = repostUsercard(mId, after);
		Long count = new Long(0);
		for(String u : usercard){
			if(fanMap.containsKey(u) && fanMap.get(u)){
				continue;
			}
				count += 1;
		}
		if(usercard.size()>0)
			return count/usercard.size();
		else 
			return count;
	}
	
	
	
	public static void writeToDB(String userId){
		DBUtil db = new DBUtil();
		Map<String, Boolean> fanMap  = new HashMap<String, Boolean>();
		fanMap = getWeaktieFan(userId);
		String weakFan = "";
		ArrayList<String> weakTie = new ArrayList<String>();
		
		for(String fan : fanMap.keySet()){
			if(!fanMap.get(fan)){
				weakFan += (fan + " ");
			}
		}
		
		String sql_query = "select userId from weakFan where userId = ?";
		List parameters = new ArrayList();
		parameters.add(userId);
		List result = db.query(sql_query, parameters);
		Boolean insert_flag = false;
		for(Object R : result){
			if(((Map<String, String>)R).get("userId") == null){
				insert_flag = true;
			}
		}
		
		String sql = "";
		List params = new ArrayList(); 
		
		
		if(insert_flag){
			System.out.println("true");
			sql = "insert weakFan(userId, weakFan) value(?,?)";
			params.add(userId);
			params.add(weakFan);
		} else {
			System.out.println("false");
			sql = "update weakFan set weakFan = ? where userId = ?";
			params.add(weakFan);
			params.add(userId);
		}
		db.update(sql, params);
		db.close();
	}
	
	
	
	public static void main(String... args){

		writeToDB("1005051740577714");
	}
	
	
}
