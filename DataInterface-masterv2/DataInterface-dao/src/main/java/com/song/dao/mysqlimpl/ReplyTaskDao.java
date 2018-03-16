package com.song.dao.mysqlimpl;

import com.song.model.mysqlmodel.ReplyTask;

import java.util.List;

public interface ReplyTaskDao {

	public abstract List<ReplyTask> getAllReplyTasks();

}