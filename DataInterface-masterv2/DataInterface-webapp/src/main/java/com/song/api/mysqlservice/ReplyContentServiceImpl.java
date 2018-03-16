package com.song.api.mysqlservice;

import com.song.api.mysqlimpl.ReplyContentService;
import com.song.dao.mysqlimpl.ReplyContentDao;
import com.song.model.mysqlmodel.ReplyContent;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;


@Service
public class ReplyContentServiceImpl implements ReplyContentService {

    @Autowired
    private ReplyContentDao replyContentDaoImpl;

    @Override
    public List<ReplyContent> getReplyContentByTaskId(int taskId) {
        return replyContentDaoImpl.getReplyContentByTaskId(taskId);
    }

    @Override
    public  List<ReplyContent> getAllReplyContents() {
        return replyContentDaoImpl.getAllReplyContents();
    }

}