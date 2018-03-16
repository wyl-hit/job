package com.song.dao.mysqlimpl;

import com.song.model.mysqlmodel.Posts;

import java.util.List;

public interface PostsDao {

	public abstract List<Posts> getPostsBySiteId(int taskId);

	public abstract List<Posts> getPostsByUrlPrefix(String urlPrefix);

	public abstract List<Posts> getAllPosts();

	public abstract String insertPosts(Posts posts);
}