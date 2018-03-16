package com.song.api.mysqlimpl;

import com.song.model.mysqlmodel.ReplyContent;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
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
@Path("/mysql/reply_content")
public interface ReplyContentService {

    @GET
    @Produces({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/reply_content/
    public abstract List<ReplyContent> getAllReplyContents();

    @GET
    @Path("/task_id/{taskId}")
    @Produces({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/reply_content/task_id/{taskId}
    public abstract List<ReplyContent> getReplyContentByTaskId(@PathParam("taskId") int taskId);



}
