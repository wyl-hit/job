package util;

/** 
 *  @Project: forecast
 *	@Title: DBUtil.java
 *	@Author: wyl
 *  @Date: Dec 21, 2016 9:44:24 PM
 * 	@Description: TODO
 *  @Version: v1.0
 */

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.DriverManager;
import java.util.logging.*;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.sql.ResultSetMetaData;

import setting.Configs;
import static setting.Configs.dbConfig;
//@problem
//@TODO
//close()函数什么时候调用？
//一旦调用close()函数则DBUtil对象即无法使用~~~
public class DBUtil {

	private final String url = Configs.getDBUrl();
	private final String driver = Configs.getDBDriver();
	private final String user = Configs.getDBUser();
	private final String password = Configs.getDBPassword();
	
	public Connection conn = null;
	public Statement stmt = null;
	ResultSet rs = null;
	
	public DBUtil(){
		try {
			Class.forName(driver);
			conn = DriverManager.getConnection(url,user,password);
			stmt = conn.createStatement();
		} catch(Exception e){
			e.printStackTrace();	
			close();
		}
	}


	public DBUtil(String source) {
		try {
			Class.forName(driver);
			switch (source) {
				case "a":
					conn = DriverManager.getConnection(
							dbConfig.get("customUrl")
									+ dbConfig.get("tableWeibo")
									+ dbConfig.get("options")
							, user, password);
					break;
				case "b":
					conn = DriverManager.getConnection(
							dbConfig.get("customUrl")
									+ dbConfig.get("tableTwitter")
									+ dbConfig.get("options")
							, user, password);
					break;
				case "c":
					conn = DriverManager.getConnection(
							dbConfig.get("customUrl")
									+ dbConfig.get("tableFacebook")
									+ dbConfig.get("options")
							, user, password);
					break;
			}
			stmt = conn.createStatement();
		} catch (Exception e) {
			e.printStackTrace();
			close();
		}
	}

	
//	------------------------------------------not test---------------------------------------
	//sqlBatch = true关闭自动提交
	public DBUtil(boolean sqlBatch){
		if(!sqlBatch){
			System.out.println("WARN:[sql batch autoCommit not close, speed will limited.]");
		}
		try{
			Class.forName(driver);
			conn = DriverManager.getConnection(url,user,password);
			conn.setAutoCommit(!sqlBatch);
			stmt = conn.createStatement();
		} catch(Exception e){
			e.printStackTrace();
			close();
		}
	}
//	------------------------------------------not test---------------------------------------
	
	//version 1
	public ResultSet query1(String sql){
		Statement stmt = this.stmt;
		try{
			rs = stmt.executeQuery(sql);
		} catch(Exception e){
			e.printStackTrace();
			close();
		}
		return rs;
	}

	// strongtieInfo
	public ResultSet rawquery(String sql){
		Statement stmt = this.stmt;
		try{
			rs = stmt.executeQuery(sql);
		} catch(Exception e){
			e.printStackTrace();
			close();
		}
		return rs;
	}

	public List<?> query(String sql){
		ResultSet rs = null;
		List resultList = null;
		Statement stmt = this.stmt;
		try{
			rs = stmt.executeQuery(sql);
			resultList = new ArrayList();
			ResultSetMetaData rsmd = rs.getMetaData();
			Map metaMap = null;
			while(null != rs && rs.next()){
				metaMap = new HashMap();
				for(int i = 1; i <= rsmd.getColumnCount(); i++){
					metaMap.put(rsmd.getColumnName(i),rs.getObject(rsmd.getColumnName(i)));
				}
				resultList.add(metaMap);
			}
		} catch(Exception e){
			e.printStackTrace();
			close();
			
		}
		return resultList;
	
	}
	
	/*
	* query example:
	* DBUtil db = new DBUtil("a");


        String sql = "select id, post_time from weibo where uid = 1730077315";
        List param = new ArrayList();
        List result = db.query(sql);

        for(Object m : result){
            Map r = (Map)m;
            System.out.println(r.get("id"));
            System.out.println(r.get("post_time"));
        }


        db.close();
	* */


	//version 2
	public List<?> query(String sql, List<?> parameters){
		ResultSet rs = null;
		List resultList = null;
		Connection conn = this.conn;
		PreparedStatement prestmt = null;
		try{
			prestmt = conn.prepareStatement(sql);
//			for(int i = 0; i < parameters.length; i++){
//				prestmt.setObject(i + 1, parameters[i]);
//			}
			int index = 0;
			for(Object p : parameters){
				prestmt.setObject(++ index, p);
			}
			
			
			rs = prestmt.executeQuery();
			resultList = new ArrayList();
			ResultSetMetaData rsmd = rs.getMetaData();
			Map metaMap = null;
			while(null != rs && rs.next()){
				metaMap = new HashMap();
				for(int i = 1; i <= rsmd.getColumnCount(); i++){
					metaMap.put(rsmd.getColumnName(i),rs.getObject(rsmd.getColumnName(i)));
				}
				resultList.add(metaMap);
			}
		} catch(Exception e){
			e.printStackTrace();
			close();
		}
		return resultList;
	}

	// 简单查询，获取一列数据
	public List<String> query1Column(String sql){
		ResultSet rs = null;
		List<String> resultList = new ArrayList<String>();
		Statement stmt = this.stmt;
		try{
			rs = stmt.executeQuery(sql);
			ResultSetMetaData rsmd = rs.getMetaData();
			while(null != rs && rs.next()){
				resultList.add(rs.getString(1));
			}
		} catch(Exception e){
			e.printStackTrace();
			close();
		}
		return resultList;
	}


	private int upDate(String sql, List<?> parameters){
		int rows = 0;
		Connection conn = this.conn;
		PreparedStatement prestmt = null;
		try{
			prestmt = conn.prepareStatement(sql);
			int i = 0;
			for(Object p : parameters){
				prestmt.setObject(++ i, p);
				rows ++;
			}
			System.out.println("[DBUtil]: <sql Params>:" + parameters);
			prestmt.executeUpdate();
		} catch(Exception e){
			e.printStackTrace();
			close();
		}
		return rows;
	}
	
	public int update(String sql, List<?> parameters){
		return upDate(sql, parameters);
	}
	
	
	public void batchInsert(String sql,List<List<?>> itemsTable){
		Connection conn = this.conn;
		PreparedStatement prestmt = null;
		try {
			conn.setAutoCommit(false);
			stmt = conn.createStatement();
			prestmt = conn.prepareStatement(sql);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			close();
		}
		
		int batchCount = 0;
		for(List<?> item : itemsTable){
			batchCount ++;
			try {
				for(int i = 1; i <= item.size(); i++)
					prestmt.setObject(i, item.get(i - 1));
				prestmt.addBatch();	
				if(0 == batchCount % Integer.parseInt(Configs.getBatchNum())){
					prestmt.executeBatch();
					prestmt.clearBatch();
					conn.commit();
					batchCount = 0;
				}
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
				close();
			}
		}
		
		try{
			prestmt.executeBatch();
			prestmt.clearBatch();
			conn.commit();
		} catch(SQLException e){
			e.printStackTrace();
		} finally{
			close();
		}
		
	}
	
	public void close(){
		try{
			if(null != rs)
				rs.close();
			if(null != stmt)
				stmt.close();
			if(null != conn)
				conn.close();
		} catch (Exception e){
			e.printStackTrace();
		} 
	}
	
	public static void main(String[] args){
//		com.twitter.crawler.model.Comment comment = null;
//		String sql = "insert into twitter_comment(comment_uid,nickname,tid,author_uid,comment_content,created_tiem,like_num,repost_num) values(?,?,?,?,?,?,?,?)";
//		List<List<?>> ll = new ArrayList<List<?>>();
//		List<?> l = new ArrayList();
//		
		
		String sql = "update twitter_comment set like_num = ?, repost_num = ? where comment_id = ? and comment_uid = ?";
		List parameters = new ArrayList();
		int like_num = 100;
		parameters.add(like_num);
		parameters.add(100);
		parameters.add("750552245956177920");
		parameters.add("mfeigin");
		DBUtil db = new DBUtil();
		db.update(sql, parameters);
		
		
		
	}
	
}
