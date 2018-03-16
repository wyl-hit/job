package com.song.dao.mysqldao;
/**
 * Created by wyl on 2015/12/13.
 */
import com.song.dao.mysqlimpl.PostsDao;
import com.song.model.mysqlmodel.Posts;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;


@Repository
public class PostsDaoImpl implements PostsDao {

	@Autowired
	private SessionFactory sessionFactory;

	public SessionFactory getSessionFactory() {
		return sessionFactory;
	}

	public void setSessionFactory(SessionFactory sessionFactory) {
		this.sessionFactory = sessionFactory;
	}

	@Override
	@Transactional
	public List<Posts> getPostsBySiteId(int siteId) {
		Session s = sessionFactory.getCurrentSession();
		return s.createQuery("select url,title,content from Posts p where  p.site_id = ?")
				.setInteger(0, siteId)
				.list();
	}

	@Override
	@Transactional
	public  List<Posts> getAllPosts() {
		return sessionFactory.getCurrentSession()
				.createQuery("from Posts")
				.list();
	}

	@Override
	@Transactional
	public  List<Posts> getPostsByUrlPrefix(String urlPrefix) {
		return sessionFactory.getCurrentSession()
				.createQuery("select url,title,content from Posts p where  p.url like ?")
				.setString(0, urlPrefix + "%")
				.list();
	}

	@Override
	@Transactional
	public String insertPosts(Posts posts) {
		Session s = sessionFactory.getCurrentSession();
		s.save(posts);
		return "Insert OK!" ;
	}

}
