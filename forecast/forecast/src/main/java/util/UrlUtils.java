/**
 * @Project:SHCrawler
 * @Title:UrlUtils.java
 * @Description:TODO
 * @autor:wing
 * @date: @2016-5-16下午7:33:50
 * @Copyright:2016 hit. All rights reserved.
 * @version:V1.0
 */
package util;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * @ClassName UrlUtils
 * @Description url工具类
 * @author wing
 * @date 2016-5-16下午7:33:50
 */
public class UrlUtils {
	private static String[] str62keys = { "0", "1", "2", "3", "4", "5", "6",
			"7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
			"k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w",
			"x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
			"K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W",
			"X", "Y", "Z" };

	/**
	 *
	 * @Description:生成用户关注列表的url
	 * @User:wyl
	 * @updatetime:2016-5-16下午8:25:11
	 *
	 */
	public static String getUserFollowingUrl(String userId){
		return "http://weibo.com/p/"+userId+"/follow?from=rel&wvr=5&loc=hisfollow";
		// 例 http://weibo.com/p/1003061087770692/follow?from=rel&wvr=5&loc=hisfollow
	}

	/**
	 *
	 * @Description:生成用户关注列表的末页url
	 * @User:wyl
	 * @updatetime:2016-5-16下午8:25:11
	 *
	 */
	public static String getUserFollowingEndUrl(String userId, int page){
		//http://weibo.cn/1608574203/follow?page=1
		return "http://weibo.cn/"+userId+"/follow?page="+Integer.toString(page);
	}
	/**
	 * 
	 * @Description:生成用户基本资料的url
	 * @User:wing
	 * @updatetime:2016-5-16下午8:25:11
	 *
	 */
	public static String getUserInfoUrl(String userId){
		return "http://weibo.cn/"+userId+"";
	}

	
	/**
	 * 
	 * @Description:微博内容第一次加载的url
	 * @User:wing
	 * @updatetime:2016-5-16下午8:25:34
	 *
	 */
	public static String getContentUrl0(String userId,int page){
		return "http://weibo.com/p/"+userId+"/home?is_all=1&page="+page+"";
		//例 http://weibo.com/p/1006051259193624/home?is_all=1&page=1;
	}
	
	
	/**
	 * 
	 * @Description:微博第一次缓冲url
	 * @User:wing
	 * @Updatetime:2016-5-16下午8:26:18
	 *
	 */
	public static String getContentUrl1(String userId,int page){
		String domain=userId.substring(0, 6);
		return "http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain="+domain+"&is_all=1&pagebar=0&id="+userId+"&page="+page+"&pre_page="+page+"";
	}
	
	/**
	 * 
	 * @Description:微博第二次缓冲url
	 * @User:wing2234
	 * @Updatetime:2016-5-16下午8:26:38
	 *
	 */
	public static String getContentUrl2(String userId,int page){
		String domain=userId.substring(0, 6);
		return "http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain="+domain+"&is_all=1&pagebar=1&id="+userId+"&page="+page+"&pre_page="+page+"";
	}
	

	/**
	 * 
	 * @Description:微博内容的高级搜索首次加载url
	 * @User:wing
	 * @Updatetime:2016-5-26下午5:11:13
	 *
	 */
	public static String getSearchContentUrl(String userId,int page){
		
		//搜索词暂为空 http://weibo.cn/1816011541?page=2
		return "http://weibo.cn/"+userId+"?page="+page+"";
	}

	public static String getSearchTopicContentUrl(String keyword,int page){
		//http://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%96%87%E7%AB%A0%E5%87%BA%E8%BD%A8&page=4
		return "http://weibo.cn/search/mblog?hideSearchFrame=&keyword="+keyword+"&sort=hot&page="+page+"";
	}
	/**
	 * 
	 * @Description:微博内容的高级搜索第二次缓冲url
	 * @User:wing
	 * @Updatetime:2016-5-30上午10:32:39
	 *
	 */
	public static String getSearchContentUrl2(String userId,int page,String start_date,String end_date){
		
		//搜索词暂为空
		String key_word="";
		String domain=userId.substring(0, 6);
		return "http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&id="+userId+"&domain="+domain+"&page="+page+"&pre_page="+page+"&pagebar=1&is_search=1&start_time="+start_date+"&end_time="+end_date+"&key_word="+key_word+"&is_ori=1&is_forward=1&is_text=1&is_pic=1&is_video=1&is_music=1&is_article=1";
		// 例 http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&id=1006051259193624&domain=100605&page=1&pre_page=1&pagebar=1&is_search=1&start_time=2016-07-23&end_time=2016-07-24&key_word=&is_ori=1&is_forward=1&is_text=1&is_pic=1&is_video=1&is_music=1&is_article=1
	}

	public static String getHotCommentUrl(String commentid,int page){
		//http://weibo.cn/comment/hot/ElA7rAlbg?rl=1&page=3
		commentid = getMidbyId(commentid);
		return "http://weibo.cn/comment/hot/"+commentid+"?rl=1?page="+page+"";
	}
	/**
	 * 
	 * @Description:微博评论的url
	 * @User:wing
	 * @Updatetime:2016-5-16下午8:41:51
	 *
	 */
	public static String getCommentUrl(String commentid,int page){
		//http://weibo.cn/comment/ElA7rAlbg
		commentid = getMidbyId(commentid);
		return "http://weibo.cn/comment/"+commentid+"?page="+page+"";
	}
	public static String getRepostUrl(String mid,int page){
		mid = getMidbyId(mid);
		//http://weibo.cn/repost/ElA7rAlbg
		return "http://weibo.cn/repost/"+mid+"?page="+page+"";
	}
	public static String getToIdUrl(String usercard){
		
		if(usercard.matches("[0-9]+"))
			return "http://weibo.com/u/"+usercard+"";
		else
			return "http://weibo.com/"+usercard+"";
		//http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=3983484152485185&max_id=3983731426887078&page=4&__rnd=1465279329564
		
	}
	public static String getExtendAccountUrl(String uid,int page){
		
		//url="http://weibo.com/p/1004061608574203/follow?page=1";
		return "http://weibo.com/p/"+uid+"/follow?page="+page+"";
		
	}
	
    public static String getFansUrl(String userid,int page){
		
		//http://weibo.cn/1608574203/fans?page=3
		return "http://weibo.cn/"+userid+"/fans?page="+page+"";
		
	}
    
    public static String getFollowingUrl(String userNum,int page){
		
		//url="http://weibo.com/p/1004061608574203/follow?page=1";
		return "http://weibo.com/"+userNum+"/follow?page="+page+"";
		
	}

	public static String getMidbyId(String mid){
		List<String> url_result = new ArrayList<String>();
		// 由mid 得到url 第一步反转mid “abcd”——>"dcba"
		String mid_reverse = new StringBuilder(mid).reverse().toString();
		int size = 0;
		if(mid_reverse.length() % 7 ==0)
			size = mid_reverse.length() / 7;
		else
			size = mid_reverse.length() / 7 + 1;
		for(int i=0; i<size; i++){
			String pos_mid = "";
			try{
				pos_mid = mid_reverse.substring(i*7, (i+1)*7);
			}
			catch (StringIndexOutOfBoundsException e){
				pos_mid = mid_reverse.substring(i*7);
			}
			pos_mid = new StringBuilder(pos_mid).reverse().toString();
			String part_url = Base62Encode(Integer.parseInt(pos_mid));
			int part_url_len = part_url.length();
			if(i < size - 1 && part_url.length()< 4)
				part_url = '0' * (4 - part_url_len) + part_url;
			url_result.add(part_url);
		}
		Collections.reverse(url_result);

		String mid_reserve = "";
		for(String one: url_result){
			mid_reserve += one;
		}
		return mid_reserve;
	}

	/**
	 *
	 * @Description: 根据用户的uid和评论的mid获取一条微博的url
	 * @User: wyl
	 * @Updatetime:2016-7-23下午15:06:51
	 * 例： 输入 用户李晨uid：1259193624 mid：3997953968045381 得到 指定微博的url：http://weibo.com/1259193624/DF6egxKYd
	 */
	public static String getWeiBoUrlByMid(String uid, String mid){
		String mid_reserve = getMidbyId(mid);
		String weibo_url = "http://weibo.cn/"+uid+"/"+mid_reserve+"";
		//http://weibo.cn/1087770692/En6ON44zl
		return weibo_url;
	}

	/**
	 *
	 * @Description: 对数据进行base62编码
	 * @User: wyl
	 * @Updatetime:2016-7-23下午19:06:51
	 */
	public static String Base62Encode(int num){
		String chrCharArray = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
		char[] ALPHABET = chrCharArray.toCharArray();;
		if (num == 0)
			return String.valueOf(ALPHABET[0]);
		List<String> arr = new ArrayList<String>();
		int base = chrCharArray.length();
		while(num>0){
			int rem = num % base;
			num = num / base;
			arr.add(String.valueOf(ALPHABET[rem]));
		}
		Collections.reverse(arr);
		String result = "";
		for(String one: arr){
			result += one;
		}
		return result;
	}
	public static String Str62toInt(String str62)
	{
		long i64 = 0;
		for (int i = 0; i < str62.length(); i++)
		{
			long Vi = (long)Math.pow(62, (str62.length() - i - 1));
			String t = str62.substring(i,i+1);

			i64 += Vi * findindex(t);
		}
		// System.out.println(i64);
		return Long.toString(i64);
	}

	public static int findindex(String t)
	{
		int index=0;
		for(int i=0;i<str62keys.length;i++)
		{
			if(str62keys[i].equals(t)){
				index=i;
				break;
			}
		}
		return index;
	}

	public static String Uid2Mid(String mid)
	{
		String id = "";
		for (int i = mid.length() - 4; i > -4; i = i - 4) //从最后往前以4字节为一组读取URL字符
		{
			int offset1 = i < 0 ? 0 : i;
			int len = i < 0 ? mid.length() % 4 : 4;

			String str = mid.substring(offset1, offset1 + len);
			// System.out.println(offset1+" "+len+" "+str);

			str = Str62toInt(str);

			if (offset1 > 0) //若不是第一组，则不足7位补0
			{
				while (str.length() < 7)
				{
					str = "0" + str;
				}
			}
			id = str + id;
		}

		return id;
	}
	public static void main(String args[]){
		UrlUtils u =new UrlUtils();
		String label = getMidbyId("4058440952767150");
	/*	String url = u.getCommentUrl("1887826884", 1);
		System.out.println(url);*/
		String a = u.Uid2Mid("Eo4a9blBD");
		System.out.println(a);
	//	String a = getSearchTopicContentUrl("文章出轨",1);
	//	System.out.println(a);

	//	System.out.println(label);


	}
}

