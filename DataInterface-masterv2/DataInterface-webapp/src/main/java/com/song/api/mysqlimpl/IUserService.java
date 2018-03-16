package com.song.api.mysqlimpl;

import com.song.model.mysqlmodel.User;

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
@Path("/mysql/users")
public interface IUserService {
    @GET
    @Produces({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/users/
    public abstract List<User> getAllUsers();

    @GET
    @Path("/{userId}")
    @Produces({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/users/{id}
    public abstract User getUserByID(@PathParam("userId") int userId);

    @PUT
    @Produces({MediaType.APPLICATION_JSON})
    @Consumes({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/users/
    public abstract String insertUser(User user);

    @POST
    @Path("/{userId}") //@NotNull @NotEmpty
    @Produces({MediaType.APPLICATION_JSON})
    @Consumes({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/users/
    public abstract String updateUser(@PathParam("userId") int userId, User user);

    @DELETE
    @Produces({MediaType.APPLICATION_JSON})
    @Consumes({MediaType.APPLICATION_JSON})
    @Path("/{userId}")
    // http://localhost:8080/DataInterface/api/users/{id}
    public abstract String deleteUser(@PathParam("userId") int userId);
}
