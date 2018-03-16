package util;

import java.sql.ResultSet;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class tranform_repost {
	public static DBUtil dbsql = new DBUtil();
	public static UrlUtils u =new UrlUtils();
	
	public static String getTureTime(String originTime, String addTime) throws ParseException {
        System.out.println("\n原时间: "+originTime);
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        SimpleDateFormat addsdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Calendar now = Calendar.getInstance();
        now.setTime(addsdf.parse(addTime));
        Date dt = now.getTime();
        //20秒前
        if(originTime.contains("秒前")) {
            System.out.println("现在时间："+sdf.format(dt));
            String secs = originTime.substring(0, originTime.indexOf("秒前")-1);
            now.add(Calendar.SECOND, -Integer.valueOf(secs.trim()));
            dt = now.getTime();
            return sdf.format(dt);
        }
        //22分钟前
        if(originTime.contains("分钟前")) {
            int tt = 0;
            originTime = originTime.trim();
            Pattern p_count=null;
            Matcher m_count=null;
            String num_Pattern = "\\d+";
            System.out.println("现在时间：" + sdf.format(dt));
            String mins = originTime.substring(0, originTime.indexOf("分钟前"));
            p_count= Pattern.compile(num_Pattern);
            m_count = p_count.matcher(mins);
            if(m_count.find())
                tt =  Integer.parseInt(m_count.group());
            now.add(Calendar.MINUTE, - tt);
            dt = now.getTime();
            System.out.println(dt);
            return sdf.format(dt);
        }
        //今天 03:08
        if(originTime.contains("今天")) {
            int index = originTime.indexOf(":");
            String hours = originTime.substring(index-2, index);
            String mins = originTime.substring(index+1, index+3);
            now.set(Calendar.HOUR_OF_DAY, Integer.valueOf(hours));
            now.set(Calendar.MINUTE, Integer.valueOf(mins.trim()));
            dt = now.getTime();
            return sdf.format(dt);
        }

        //8月8日 23:05
        if(originTime.contains("月") && originTime.contains("日")) {
            Pattern p_count=null;
            Matcher m_count=null;
            String num_Pattern = "\\d+";
            int monthIndex = originTime.indexOf("月");
            int dayIndex = originTime.indexOf("日");
            int index = originTime.indexOf(":");
            int month_m = 0;
            int day_m = 0;
            int hour_m =0;
            int mins_m = 0;
            String month = originTime.substring(0, monthIndex);
            String day = originTime.substring(monthIndex+1, dayIndex);
            String hours = originTime.substring(dayIndex+2, index);
            String mins = originTime.substring(index+1, originTime.length()-1);
            p_count= Pattern.compile(num_Pattern);
            m_count = p_count.matcher(month);
            if(m_count.find())
                month_m =  Integer.parseInt(m_count.group());

            m_count = p_count.matcher(day);
            if(m_count.find())
                day_m =  Integer.parseInt(m_count.group());
            m_count = p_count.matcher(hours);
            if(m_count.find())
                hour_m = Integer.parseInt(m_count.group());
            m_count = p_count.matcher(mins);
            if(m_count.find())
                mins_m = Integer.parseInt(m_count.group());
            now.set(Calendar.MONTH, month_m-1);
            now.set(Calendar.DAY_OF_MONTH, day_m);
            now.set(Calendar.HOUR_OF_DAY, hour_m);
            now.set(Calendar.MINUTE, mins_m);
            dt = now.getTime();
            return sdf.format(dt);
        }

        //2014-10-27 18:33
        if(originTime.contains("-")) {
            return originTime;
        }

        return originTime;
    }
	
	public static void main(String ...strings ) throws Exception{
		HashMap<String, String> msgidList = new HashMap<String, String>();
		String writesql = "select id, wid, add_time, repost_time from repost3";
		ResultSet rs = null;
		try{
			rs = dbsql.query1(writesql);
			while(null != rs && rs.next()){
//			userMsgShareDetail.add(new MsgShareDetail(rs.getString("repost_usercard"), rs.getInt("repost_likeNum"), rs.getInt("repost_reNum"), rs.getTimestamp("repost_time")));
				msgidList.put(rs.getString("id"), rs.getString("wid")+"," +rs.getString("add_time")+","+rs.getString("repost_time"));
			}
			rs.close();
		} catch(Exception e){
			System.out.println("*****************");
			System.out.println(writesql);
			System.out.println("*****************");
			e.printStackTrace();
		}
		for(String oldid:msgidList.keySet()){
			String widString = msgidList.get(oldid).split(",")[0].split("_")[2];
			String add_time = getTureTime(msgidList.get(oldid).split(",")[2], msgidList.get(oldid).split(",")[1]);
			String updateSQL = "update repost3 set wid='" + u.Uid2Mid(widString) + "',from_uid='" + msgidList.get(oldid).split("_")[0] + "',repost_time='"+add_time+"' where id='"+oldid+"'";
			try{
				dbsql.stmt.execute(updateSQL);
			}catch(Exception e){
				System.out.println("*****************");
				System.out.println(updateSQL);
				System.out.println("*****************");
				e.printStackTrace();
			}
		}
		dbsql.close();
	}
}
