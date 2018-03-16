package com.song.api.mongoservice;

/**
 * Created by song on 2015/12/22.
 */
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
@RequestMapping("/user")
public class MongoControl {

    @RequestMapping(value="welcome",method=RequestMethod.POST)
    public String printMessage() {

        return "users";
    }
}
