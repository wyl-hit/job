package com.song.api.monogoimpl;
import com.song.model.mongomodel.MongoPosts;
import org.codehaus.jettison.json.JSONObject;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
//import com.song.dao.mongoimpl.BaseDaoI;
import javax.servlet.http.HttpServletRequest;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import java.util.List;
/**
 * Created by song on 2015/12/13.
 */
@Path("/mongo/posts")

@RequestMapping(value = "/mongo/posts")
public interface IMongoPut {

    @POST

    @Produces({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/mongo/put/
    public abstract String  insertdata();

    //@GET
    @RequestMapping(method = RequestMethod.GET)
    @Produces({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/mongo/put/
    public abstract List<MongoPosts> getdata();

}
