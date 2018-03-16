package com.song.dao.mongoimpl;
import com.song.model.mongomodel.MongoPosts;

import java.util.List;

/**
 * Created by wyl on 2015/12/16.
 */
public interface BaseDaoI<T> {
    public abstract T insert(T t) ;
    public List<MongoPosts> getdata() ;
}
