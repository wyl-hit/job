package com.song.dao.mysqldao;
/**
 * Created by wyl on 2015/12/13.
 */
import com.song.dao.mysqlimpl.IUserDao;
import com.song.model.mysqlmodel.User;
import org.hibernate.Query;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;


@Repository
public class UserDaoImpl  implements IUserDao {

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
	public List<User> getAllUsers() {
		List<User> users = sessionFactory.getCurrentSession().createCriteria(User.class).list();
		return users;
	}

	@Override
	@Transactional
	public User getUserByID(int userId) {
		Session s = sessionFactory.getCurrentSession();
		User user = (User) s.get(User.class, userId);
		return user;
	}


	@Override
	@Transactional
	public String insertUser(User user) {
		Session s = sessionFactory.getCurrentSession();
		int userId = (int) s.save(user);
		return "Insert OK, ID: " + userId;
	}

	@Override
	@Transactional
	public String updateUser(int userId, User user) {
		Session s = sessionFactory.getCurrentSession();
		user.setId(userId);
		s.update(user);
		return "Update OK, ID: " + userId;
	}

	@Override
	@Transactional
	public String deleteUser(int userId) {
		Session s = sessionFactory.getCurrentSession();
//		sessionFactory.getCurrentSession().delete(customer);
		Query q = s.getNamedQuery("users.deleteUser");
		q.setInteger("id", userId);
		q.executeUpdate();
		return "Delete OK, ID: " + userId;
	}
}
