package com.song.dao.mysqldao;
/**
 * Created by wyl on 2015/12/13.
 */
import com.song.dao.mysqlimpl.ReplyContentDao;
import com.song.model.mysqlmodel.ReplyContent;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;


@Repository
public class ReplyContentDaoImpl implements ReplyContentDao {

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
	public List<ReplyContent> getReplyContentByTaskId(int taskId) {
		Session s = sessionFactory.getCurrentSession();
		return s.createQuery("select content from ReplyContent r where  r.task_id = ?")
				.setInteger(0,taskId)
				.list();
	}

	@Override
	@Transactional
	public  List<ReplyContent> getAllReplyContents() {
		return sessionFactory.getCurrentSession()
				.createQuery("from ReplyContent")
				.list();
	}

}
