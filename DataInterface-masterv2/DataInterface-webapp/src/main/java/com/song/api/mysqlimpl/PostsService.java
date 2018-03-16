package com.song.api.mysqlimpl;

import com.song.model.mysqlmodel.Posts;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import java.util.List;

/**
 *
 * CRUD Operations:
 *  - Create - PUT
 *  - Read   - GET
 *  - Update - POST
 *  - Delete - DELETE
 * @author wyl
 *
 */
@Path("/mysql/posts")
public interface PostsService {

    @GET
    //@Produces 注释被针对 Accept 请求头进行匹配以决定客户机是否能够处理由给定方法返回的表示。
    @Produces({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/posts/
    public abstract List<Posts> getAllPosts();

    @GET
    @Path("/site_id/{siteId}")
    @Produces({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/posts/site_id/{siteId}
    public abstract List<Posts> getPostsBySiteId(@PathParam("siteId") int siteId);

    @GET
    @Path("/url_prefix/{urlPrefix}")
    @Produces({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/posts/url_prefix/{urlPrefix}
    public abstract List<Posts> getPostsByUrlPrefix(@PathParam("urlPrefix") String urlPrefix);

    @PUT
    @Produces({MediaType.APPLICATION_JSON})
    @Consumes({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/posts/
    public abstract String insertPosts(Posts posts);

}
