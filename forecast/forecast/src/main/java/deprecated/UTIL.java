package deprecated;

import util.DBUtil;
import util.FileUtil;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by wyl on 2017/2/21.
 */
public class UTIL {
    public static void main(String[] args){
        String file = "D://data/sql";

        String result = FileUtil.read(file);

        String[] lines = result.split(";");
        DBUtil db = new DBUtil("b");


        for(String line: lines){
            String l = line.substring(line.indexOf('\'') + 1,line.lastIndexOf('\''));
            String[] i2n = l.split(",");
            System.out.println(l);
            String id = i2n[0].substring(0, i2n[0].lastIndexOf('\''));
            String name = i2n[1].substring(i2n[1].indexOf('\'') + 1, i2n[1].length());
            System.out.println(id + " " + name);
            String sql = "update user set uid = ? where screenName = ?";
            List params = new ArrayList();
            params.add(id);
            params.add(name);
            db.update(sql, params);
        }
        db.close();

    }

}
