package util;
/** @author wyl
 * created at 2016/05/23
 * 将任意语言翻译成中文，也可指定翻译的源语言与目的语言
 * pro:翻译结果返回应为一个list，实际返回一个字符串
 * 输入检测:·空 ·http	·www
*/
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.HttpException;
import org.apache.commons.httpclient.NameValuePair;
import org.apache.commons.httpclient.methods.GetMethod;

import com.google.gson.Gson;

public class Translate {
	private static final String url = "http://fanyi.baidu.com/transapi";
	public static GetMethod method = new GetMethod(url);
	public static HttpClient client = new HttpClient();
	
	
	
	public static String translate(String source) throws Exception {
		if(isChineseChar(source)){
			return source;
		}
    	method.setQueryString(new NameValuePair[]{
    			new NameValuePair("from","auto"),
    			new NameValuePair("to","zh"),
    			new NameValuePair("query",source)
    	});
    	
    	List<String> dstResult = new ArrayList<String>();
    	for(Data ds : getResult(method)){
    		dstResult.add(ds.getDst());
    	}
    	return dstResult.get(0);
    }
	
	public static String translate(String source, String from, String to) throws Exception{
		if(isChineseChar(source)){
			return source;
		}
    	method.setQueryString(new NameValuePair[]{
    			new NameValuePair("from",from),
    			new NameValuePair("to",to),
    			new NameValuePair("query",source)
    	});
    	
    	List<String> dstResult = new ArrayList<String>();
    	for(Data ds : getResult(method)){
    		dstResult.add(ds.getDst());
    	}
    	return dstResult.get(0);
    }
	
	public static boolean isChineseChar(String str){
	       Pattern p=Pattern.compile("[\u4e00-\u9fa5]"); 
	       Matcher m=p.matcher(str); 
	       return m.find();	       
	}
	
	
	public static List<Data> getResult(GetMethod method) throws HttpException, IOException{
		client.executeMethod(method);
    	String response = new String(method.getResponseBodyAsString());
    	method.releaseConnection();
    	
    	Gson gson = new Gson();
    	TranslateMode translateMode = gson.fromJson(response, TranslateMode.class);
    	return translateMode.getData();
	}
	
	public static void main(String... args)throws Exception{
		test();
	}
	
	
	//测试
	public static void test() throws Exception{
		List<String> src = new ArrayList<String>(){
			{
				add("moonlight");
				add("java is a nice language");
				add("learn to write program in spark");
				add("translate test");
				add("이건 테스트");
				add("翻译测试");
			}
		};
		
		List<String> rs = null;
		for(String s : src){
			if(!isChineseChar(s))
				System.out.println(translate(s).toString());
			else
				System.out.println(s);
		}
	}
}

class Data{
	String dst, src;
	
	public String getDst(){
		return dst;
	}
	public void setDst(String dst){
		this.dst = dst;
	}
	public String getSrc(){
		return src;
	}
	public void setSrc(String src){
		this.src = src;
	}
}


class TranslateMode{
	String from, to;
	List<Data> data;
	
	public String getFrom(){
		return from;
	}
	public void setFrom(String from){
		this.from = from;
	}
	public String getTo(){
		return to;
	}
	public void setTo(String to){
		this.to = to;
	}
	public List<Data> getData(){
		return data;
	}
	public void setData(List<Data> data){
		this.data = data;
	}
}