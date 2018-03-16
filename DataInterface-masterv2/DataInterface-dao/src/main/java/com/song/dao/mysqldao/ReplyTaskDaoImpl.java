package com.song.dao.mysqldao;
/**
 * Created by wyl on 2015/12/13.
 */
import com.song.dao.mysqlimpl.ReplyTaskDao;
import com.song.model.mysqlmodel.ReplyTask;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;


@Repository
public class ReplyTaskDaoImpl implements ReplyTaskDao {

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
	public List<ReplyTask> getAllReplyTasks() {
		return sessionFactory.getCurrentSession()
				.createQuery("select id,name from ReplyTask")
				.list();
	}

}
