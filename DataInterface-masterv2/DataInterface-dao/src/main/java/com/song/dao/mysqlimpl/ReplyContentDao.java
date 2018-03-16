package com.song.dao.mysqlimpl;

import java.util.List;
import com.song.model.mysqlmodel.ReplyContent;

public interface ReplyContentDao {

	public abstract List<ReplyContent> getReplyContentByTaskId(int taskId);

	public abstract List<ReplyContent> getAllReplyContents();

}