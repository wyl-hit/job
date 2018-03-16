package com.song.api.mysqlservice;

import com.song.api.mysqlimpl.PostsService;
import com.song.dao.mysqlimpl.PostsDao;
import com.song.model.mysqlmodel.Posts;   // 初始化 model
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import java.util.List;


@Service
public class PostsServiceImpl implements PostsService {

    @Autowired
    private PostsDao postsDaoImpl;      //实例化 dao 接口

    @Override
    public List<Posts> getPostsBySiteId(int siteId) {
        return postsDaoImpl.getPostsBySiteId(siteId);
    }

    @Produces({MediaType.APPLICATION_JSON})
    @Override
    public  List<Posts> getAllPosts() {
        return postsDaoImpl.getAllPosts();
    }

    @Override
    public  List<Posts> getPostsByUrlPrefix(String urlPrefix) {
        return postsDaoImpl.getPostsByUrlPrefix(urlPrefix);
    }

    @Override
    public String insertPosts(Posts posts) {
        return postsDaoImpl.insertPosts(posts);
    }
}