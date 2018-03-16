package com.song.api.mysqlservice;

import com.song.api.mysqlimpl.ReplyTaskService;
import com.song.dao.mysqlimpl.ReplyTaskDao;
import com.song.model.mysqlmodel.ReplyTask;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;


@Service
public class ReplyTaskServiceImpl implements ReplyTaskService {

    @Autowired
    private ReplyTaskDao replyTaskDaoImpl;

    @Override
    public List<ReplyTask> getAllReplyTasks() {
        return replyTaskDaoImpl.getAllReplyTasks();
    }


}