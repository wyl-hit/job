package com.song.api.mongoservice;
import com.mongodb.*;
import com.mongodb.util.JSON;
import com.song.api.monogoimpl.IMongoPut;
import com.song.dao.mongodao.BaseDaoImpl;

import com.song.model.mongomodel.MongoPosts;
import org.apache.commons.io.IOUtils;
import org.codehaus.jettison.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import javax.servlet.http.HttpServletRequest;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.net.UnknownHostException;
import java.util.List;

/**
 * Created by song on 2015/12/13.
*/
@Service
public class MongoPut implements IMongoPut {
    @Autowired
    private BaseDaoImpl BaseDaoI;
    @Autowired
    private  HttpServletRequest request;
    public DBCollection collection;
    public Mongo mongo;
    public MongoPut() throws UnknownHostException, MongoException
    {
        mongo = new Mongo();


        DB db = mongo.getDB("test_mongodb");

        // get a single collection
        collection  = db.getCollection("person");
    }



    @RequestMapping(method = RequestMethod.POST)
    public String insertdata() {
        //System.out.println(request);
        //
        StringBuffer sb = new StringBuffer();
        BufferedReader bufferedReader = null;
        String content = "";

        try {
            bufferedReader =  request.getReader() ; //new BufferedReader(new InputStreamReader(inputStream));
            char[] charBuffer = new char[128];
            int bytesRead;
            while ( (bytesRead = bufferedReader.read(charBuffer)) != -1 ) {
                sb.append(charBuffer, 0, bytesRead);
            }


        } catch (IOException ex) {

        } finally {
            if (bufferedReader != null) {
                try {
                    bufferedReader.close();
                } catch (IOException ex) {

                }
            }
        }

        content = sb.toString();
        DBObject dbObject =(DBObject) JSON.parse(content);
        collection.insert(dbObject);
        return content;
        //




    }
    @Override
    public List<MongoPosts> getdata() {

        return BaseDaoI.getdata();


    }
}

