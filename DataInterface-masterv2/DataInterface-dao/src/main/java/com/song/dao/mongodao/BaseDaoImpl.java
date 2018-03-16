package com.song.dao.mongodao;

/**
 * Created by wyl on 2015/12/13.
 */
import java.io.File;
import java.io.IOException;
import java.lang.reflect.ParameterizedType;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.mongodb.DBObject;
import com.mongodb.util.JSON;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.data.domain.Sort.Direction;
import org.springframework.data.domain.Sort.Order;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Repository;

import com.mongodb.DB;
import com.song.dao.mongoimpl.BaseDaoI;
import com.mongodb.gridfs.GridFS;
import com.mongodb.gridfs.GridFSDBFile;
import com.mongodb.gridfs.GridFSInputFile;
import com.song.model.mongomodel.MongoPosts;
@Repository
public class BaseDaoImpl<T> implements BaseDaoI<T>  {


    @Autowired
    private MongoTemplate mongoTemplate;

    @Override
    public List<MongoPosts> getdata() {
       return this.mongoTemplate.findAll(MongoPosts.class);
    }


    @Override
    public T insert(T t) {
        try {

            this.mongoTemplate.insert(t);
        }
        catch(Exception e){
            System.out.println("*****************************************");
            System.out.println(e);
        }

        return t;
    }



}
