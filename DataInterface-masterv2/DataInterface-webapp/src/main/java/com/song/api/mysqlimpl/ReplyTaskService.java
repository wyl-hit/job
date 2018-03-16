package com.song.api.mysqlimpl;

import com.song.model.mysqlmodel.ReplyTask;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
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
@Path("/mysql/reply_task")
public interface ReplyTaskService {
    @GET
    @Produces({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/reply_task/
    public abstract List<ReplyTask> getAllReplyTasks();


}
