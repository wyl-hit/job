package com.song.api.mysqlimpl;

import com.song.model.mysqlmodel.Site;

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
 * @author Wyl
 *
 */
@Path("/mysql/site")
public interface SiteService {

    @GET
    @Produces({MediaType.APPLICATION_JSON})
    // http://localhost:8080/DataInterface/api/site/
    public abstract List<Site> getAllSites();




}
