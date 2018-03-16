package com.song.dao.mysqldao;
/**
 * Created by wyl on 2015/12/13.
 */
import com.song.model.mysqlmodel.Site;
import com.song.dao.mysqlimpl.SiteDao;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;


@Repository
public class SiteDaoImpl implements SiteDao {

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
	public  List<Site> getAllSites() {
		return sessionFactory.getCurrentSession()
				.createQuery("select site_id,site_name,site_url from Site")
				.list();
	}

}
