package deprecated;

import java.sql.Timestamp;

public class MsgShareDetail{
	public String shareFanId;
	public int likeCount;
//	public int shareCount;
	public Timestamp shareTime;
//	public MsgShareDetail(String shareFanId, int likeCount, int shareCount, Timestamp shareTime){
	public MsgShareDetail(String shareFanId, int likeCount, Timestamp shareTime){
		this.shareFanId = shareFanId;
		this.likeCount = likeCount;
//		this.shareCount = shareCount;
		this.shareTime = shareTime;
	}
}