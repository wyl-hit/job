package com.song.api.mysqlservice;

import com.song.api.mysqlimpl.SiteService;
import com.song.dao.mysqlimpl.SiteDao;
import com.song.model.mysqlmodel.Site;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;


@Service
public class SiteServiceImpl implements SiteService {

    @Autowired
    private SiteDao siteDaoImpl;

    @Override
    public  List<Site> getAllSites() {
        return siteDaoImpl.getAllSites();
    }

}