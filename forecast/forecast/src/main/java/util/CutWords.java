package util;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

//import org.ansj.domain.Result;
import org.ansj.domain.Term;
import org.ansj.splitWord.analysis.ToAnalysis;  
/** @author wyl
 * @created 2016/06/19
 *  分词模块
 *  使用ansj分词系统，将接收的文本数据切分成单词
 *  cutWords 返回利用空格隔开的单词文本串
 *  getKeyWords 返回出现次数最多的三个单词
 * 
*/
public class CutWords {
	static ToAnalysis analysis = new ToAnalysis();
	static final String symbol = "[]$^()-=~！@#￥%…&*（）—+·{}|：“”《》？：:【】、；‘’，。.,、+";
	static Map<String, Boolean> symbolChar = new HashMap<String, Boolean>();
	static HashMap<String, String> stopWords = new HashMap<String, String>();
	static String stopwordsPath = "src/main/resources/stopwords.txt";

	static {for(int i = 0; i< symbol.length(); i++){
		String ch = String.valueOf(symbol.charAt(i));
		symbolChar.put(ch, true);
	}};
	
	public CutWords(){
		

		
		
		
		
		FileInputStream fileInputStream = null;
		BufferedReader bufferedReader = null;
		try{
			File file = new File("src/main/resources/stopwords.txt");
			fileInputStream = new FileInputStream(file);
			bufferedReader = new BufferedReader(new InputStreamReader(fileInputStream));
			String stopWord;
			while((stopWord = bufferedReader.readLine()) != null){
				stopWords.put(stopWord, "_stop");
			} 
		} catch(IOException e){
			e.printStackTrace();
		} finally{
			try {
				bufferedReader.close();
				fileInputStream.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
	}
	/**
	 * 	利用ansj将文本分词，返回单词列表
	 * */
	public static List<String> getWords(String text){
		List<String> wordList = new ArrayList<String>();
		text.replace('\n', ' ').replace('\t', ' ');
		List<Term>cutResultList = analysis.parse(text);
//      Result cutResultList = analysis.parse(text);
		for(Term t : cutResultList){
			String name = t.getName();
			if(symbolChar.containsKey(name)) {
				System.out.println(name);
					continue;
			}
			wordList.add(name);
		}
		return wordList;
	}
	
	
	public static String cutWords(String text){
		String result = "";
		for(String word : getWords(text)){
			result += (word + " ");
		}
		return result;
	}
	
	/**
	 * 去除停用词后 
	 * 返回文本中前三个出现次数最多的单词作为关键字
	 * 
	*/
	public static List<String> getKeyWords(String text){
		List<String> keyWordsList = new ArrayList<String>();
		Map<String, Integer> wordMap = new HashMap<String, Integer>(); 
		for(String word : getWords(text)){
			if(stopWords.containsKey(word))
				continue;
			if(wordMap.containsKey(word))
				wordMap.put(word, wordMap.get(word) + 1);
			else
				wordMap.put(word, 1);
		}
		for(int i = 0; i < 3; i++){
			int Max = 0;
			String tempWord = null;
			for(String word : wordMap.keySet()){
				if(wordMap.get(word) > Max){
					Max = wordMap.get(word);
					tempWord = word;
				}
			}
			keyWordsList.add(tempWord);
			wordMap.remove(tempWord);
		}
		return keyWordsList;
	}
	
	
	
	//测试
	public static void test(){  
        String[] sentences = {
        		"在训练场上，即将远赴澳大利亚参加陆军轻武器技能大赛的我国参赛选手正在紧张备战。 参加这次比赛的一些国家是属于射击俱乐部的专业队，常年备战，实力强悍，想要超越他们，夺得金牌，难度可想而知。 即将出国比赛，集训选手们要做哪些准备？",
        		//"【与世隔绝做测试 体验泛亚NVH试验中心】NVH试验，看似仅仅是为了简单找出振动源与噪声源，实际在其中的学问不少。每个试验室各有所用，相互配合，汇总出一台车的NVH数据。严谨的试验条件等都是为了未来优化车辆静谧性的有效依据。",
        		//"詹姆斯带领骑士上演惊天逆转！在刚刚结束的NBA总决赛抢七大战中，克里夫兰骑士队以93比89击败金州勇士队，在总比分1比3落后情况下，连扳3场，夺得NBA总冠军。恭喜骑士队，恭喜詹姆斯，一次激动人心的夺冠之旅！",
		};
//        for(String words : sentences){
////        	String keyWords = getKeyWords(words).toString();
//        	System.out.println("微博原文 ： " + words);
////        	System.out.println("提取关键字 ： " + keyWords);
//        }
		
        for(String sentence : sentences){
        	System.out.println(cutWords(sentence));
        }
//        Consumer consumer = new Consumer("forecastMessageKeyWords");
//    	String sentence = null;
//        while(true){
////        	sentence = consumer.recieve();
//        	System.out.println(sentence);
//        	if(null != sentence)
//        		System.out.println(getKeyWords(sentence));
//        }
	 }
	
	public static void main(String[] args){


		test();
	}
}
