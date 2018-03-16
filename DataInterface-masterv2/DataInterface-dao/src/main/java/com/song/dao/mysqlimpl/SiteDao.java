package com.song.dao.mysqlimpl;
/**
 * Created by wyl on 2015/12/13.
 */
import com.song.model.mysqlmodel.Site;

import java.util.List;

public interface SiteDao {

	public abstract List<Site> getAllSites();

}