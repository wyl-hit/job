package util;

import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import setting.Configs;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static util.HbaseUtil.Trans;

/**
 * Created by wyl on 2017/2/8.
 * TODO 完成count groupby等功能
 */
public class HQuery {
    /**
     * TODO
     */

    public void weaktieQuerySample() {
        /**
         * the first step
         */
        String uid = "1234567890";
        //需要先计算出某个时间戳，表示想得到在该时间之后的原文，即最近的原文
        String timestamp = String.valueOf("3456193652346");
        HQuery UserToOrigin = new HQuery()
                .Select("id", "posttime")
                .From("ba")//From("aa")
                .Where("uid = " + uid, "posttime < " + timestamp);
        ArrayList<ArrayList<String>> origins = UserToOrigin.QueryWithRowkey();
        for (ArrayList<String> origin : origins) {//此处的for循环可以采用worker机制取代

            /**
             * the second step
             */
            HQuery OriginToRepost = new HQuery()
                    .Select("toid")
                    .From("bc")//From("ac")
                    .Where("frommid = " + origin.get(0));
            ArrayList<ArrayList<String>> reposts = OriginToRepost.Query();
            for (ArrayList<String> repost : reposts) {
                /**
                 * 根据toid统计转发次数...
                 */
            }
            OriginToRepost.close();
        }
        UserToOrigin.close();
    }

    public void featureQuerySample() {
        //得到某条消息的原文id
        String tid = "17736428346";
        //根据原文时间和特征时间点得到时间戳，小于时间戳即表示转发在时间范围内
        String reposttimestamp = "438257042304";
        HQuery OriginToRepost = new HQuery()
                .Select("toid", "repostnum", "likenum")
                .From("bc")//From("ac")
                .Where("frommid = " + tid, "posttime < " + reposttimestamp);
        ArrayList<ArrayList<String>> reposts = OriginToRepost.Query();
        for (ArrayList<String> repost : reposts) {
            /**
             * 根据uid、toid判断是否弱连接...
             */
        }
        OriginToRepost.close();
    }


    public static void main(String[] args) {
        //获取一个用户某时间段至今的原文列表
//        HQuery hQuery = new HQuery()
//                .Select("id", "posttime")
//                .From("ba")
//                .Where("uid = 14534705346", "posttime > 185678554236");

        //获取一条原文发布后某时间段的转发列表
        HQuery hQuery1 = new HQuery()
                .Select("toid", "posttime", "likenum")
                .From("bc")
                .Where("frommid = 549675966656245", "posttime < 82964043561234");

        hQuery1.RawQuery();
//        ArrayList<ArrayList<String>> results = hQuery.Query();
//        for (ArrayList<String> line : results) {
//            System.out.println("<RowKey> : " + line.get(0));
//            for (int i = 1; i < line.size(); ++i)
//                System.out.println("<col: " + hQuery.columns.get(i - 1) + "> : " + line.get(i));
//        }
//        hQuery.close();
//        hQuery1.close();
    }


    /**
     * 小批量（返回数据不多）查询时推荐使用，结果不包含rowkey
     *
     * @return
     */
    public ArrayList<ArrayList<String>> Query() {
        if (-1 != stage) {
            ArrayList<ArrayList<String>> ret = new ArrayList<ArrayList<String>>();
            ResultScanner rawresults = RawQuery();
            for (Result result : rawresults) {
                ArrayList<String> line = new ArrayList<String>();
                List<Cell> cells = result.listCells();
                if (0 < cells.size())
                    for (Cell cell : cells)
                        line.add(Trans(CellUtil.cloneValue(cell)));
                ret.add(line);
            }
            if (null != resultScanner)
                resultScanner.close();
            return ret;
        }
        return null;
    }

    /**
     * 小批量（返回数据不多）查询时推荐使用，结果包含rowkey，在每行的第一个位置
     *
     * @return
     */
    public ArrayList<ArrayList<String>> QueryWithRowkey() {
        if (-1 != stage) {
            ArrayList<ArrayList<String>> ret = new ArrayList<ArrayList<String>>();
            ResultScanner rawresults = RawQuery();
            for (Result result : rawresults) {
                ArrayList<String> line = new ArrayList<String>();
                List<Cell> cells = result.listCells();
                if (0 < cells.size()) {
                    line.add(Trans(CellUtil.cloneRow(cells.get(0))));
                    for (Cell cell : cells)
                        line.add(Trans(CellUtil.cloneValue(cell)));
                }
                ret.add(line);
            }
            if (null != resultScanner)
                resultScanner.close();
            return ret;
        }
        return null;
    }

    /**
     * 大批量（返回数据多）查询时使用。一定要记得关闭和【resultScanner】! ! !
     *
     * @return
     */
    public ResultScanner RawQuery() {
        if (-1 != stage) {
            String startrk = "", stoprk = "";
            char type = Prefix.charAt(1);
            String commrk = "";
            switch (type) {
                case 'a': //ORIGIN
                    commrk = Prefix + columns.get("uid").Value;
                    if (columns.get("posttime").Condition &&
                            (">").equals(columns.get("posttime").Operator)) {
                        startrk = commrk + DELIMITER + columns.get("posttime").Value;
                        stoprk = commrk + DELIMITER + ":";
                    } else {
                        startrk = commrk + "^";
                        stoprk = commrk + "`";
                    }
                    break;
                case 'c': //REPOST
                    commrk = Prefix + columns.get("frommid").Value;
                    if (columns.get("posttime").Condition &&
                            ("<").equals(columns.get("posttime").Operator)) {
                        startrk = commrk + DELIMITER + "/";
                        stoprk = commrk + DELIMITER +
                                String.valueOf(
                                        Long.parseLong(
                                                columns.get("posttime").Value) + 1);
                    } else {
                        startrk = commrk + "^";
                        stoprk = commrk + "`";
                    }
                    break;
            }
            if (!(startrk.equals("") || stoprk.equals(""))) {
                List<String> cols = new ArrayList<String>();
                for (String colname : columns.keySet())
                    if (columns.get(colname).Select)
                        cols.add(colname);
//                System.out.println("START ROWKEY: " + startrk +
//                        "\n STOP ROWKEY: " + stoprk);
                return hbaseUtil.query(TableForecast, startrk, stoprk, "message", cols);
            }
        }
        /**
         * resultScanner使用后，记得
         *
         * hQuery.resultScanner.close();
         * HQuery.hbaseUtil.close();
         *
         */
        return null;
    }


    class Col {
        boolean Select;
        boolean Distinct;
        boolean Condition;
        String Operator;
        String Value;
        boolean Count;

        public Col(boolean slct, boolean dstc, boolean cdt, boolean cnt) {
            this.Select = slct;
            this.Distinct = dstc;
            this.Condition = cdt;
            this.Count = cnt;
        }

        public void setCondition(String op, String val) {
            this.Condition = true;
            this.Operator = op;
            this.Value = val;
        }

        public void setCount() {
            this.Count = true;
        }

    }

    private static final String TableForecast = "forecast";
    private static final String DELIMITER = "_";
    private int stage;
    public ResultScanner resultScanner = null;
    public Result result = null;
    public Result[] results = null;
    private String Prefix = null;
    public Map<String, Col> columns = null;//<ColName, ColProperty>
    public static HbaseUtil hbaseUtil = null;

    public static void close() {
        if (hbaseUtil != null)
            hbaseUtil.close();
    }

    public HQuery() {
        if (null == hbaseUtil)
            hbaseUtil = new HbaseUtil().family(Configs.tableName);
    }

    public HQuery Select(String... cols) {
        int current = 1;
        if (this.stage < current) {
            this.stage = current;
            columns = new HashMap<String, Col>();
            for (String s : cols) {
                String[] param = s.split(" ");
                switch (param.length) {
                    case 0:
                        SyntaxError("SELECT");
                        break;
                    case 1:
                        columns.put(s, new Col(true, false, false, false));
                        break;
                    case 2:
                        if ("distinct" == param[0] || "DISTINCT" == param[0])
                            columns.put(param[1], new Col(true, true, false, false));
                        if ("count" == param[0] || "COUNT" == param[0])
                            columns.put(param[1], new Col(true, false, false, true));
                        break;
                    case 3:
                        columns.put(param[2], new Col(true, true, false, true));
                        break;
                }
            }
        } else SyntaxError("SELECT");
        return this;
    }

    public HQuery From(String type) {
        int current = 3;
        if (this.stage < current) {
            this.stage = current;
            this.Prefix = type;
        } else SyntaxError("FROM");
        return this;
    }

    public HQuery Where(String... conditions) {
        int current = 4;
        if (this.stage < current) {
            this.stage = current;
            for (String cond : conditions) {
//                System.out.print(cond+"\n");
                String[] param = cond.split(" ");
                if (3 == param.length) {
                    boolean select = false;
                    for (String colname : columns.keySet())
                        if (param[0] == colname) {
                            Col tmp = columns.get(colname);
                            tmp.setCondition(param[1], param[2]);
                            columns.put(colname, tmp);
                            select = true;
                            break;
                        }
                    if (!select) {
                        Col tmp = new Col(false, false, true, false);
                        tmp.setCondition(param[1], param[2]);
                        columns.put(param[0], tmp);
                    }
                } else SyntaxError("WHERE param.length");
            }
        } else SyntaxError("WHERE stage");
        return this;
    }

    //TODO
//    public HQuery GroupBy(String... cols) {
//        int current = 5;
//        if (this.stage < current) {
//            this.stage = current;
//
//        } else SyntaxError();
//        return this;
//    }
//
//    public HQuery OrderBy(String... cols) {
//        int current = 6;
//        if (this.stage < current) {
//            this.stage = current;
//
//        } else SyntaxError();
//        return this;
//    }
//
//    public HQuery Having(String conditions) {
//        int current = 7;
//        if (this.stage < current) {
//            this.stage = current;
//
//        } else SyntaxError();
//        return this;
//    }
//
//    public HQuery Limit(int limit) {
//        int current = 8;
//        if (this.stage < current) {
//            this.stage = current;
//
//        } else SyntaxError();
//        return this;
//    }

    private void SyntaxError() {
        this.stage = -1;
        System.out.println("Syntax ERROR ! ! ! !");
    }

    private void SyntaxError(String caller) {
        SyntaxError();
        System.out.println("ERROR IN " + caller + " ! ! ! !");
    }


}
