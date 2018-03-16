
package util;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.filter.*;
import org.apache.hadoop.hbase.filter.CompareFilter.CompareOp;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;


public class HbaseUtil {
    private static Configuration config = null;
    private Connection connection = null;
    private String tableName = null;
    private String familyName = null;
    private List<String> columns = null;
    private List<String> fields = null;

    static {
    	config = HBaseConfiguration.create();
    	config.set("hbase.zookeeper.quorum", "192.168.18.206,192.168.18.207,192.168.18.208");
    	config.set("hbase.zookeeper.property.clientPort", "2181");
    	config.set("hbase.master", "hdfs://192.168.18.206:60000");
    	config.set("hbase.root.dir", "hdfs://192.168.18.206:9000/hbase");
    }

    public HbaseUtil() {
        setConnection();
    }

    public HbaseUtil(String table) {
        setConnection();
        this.setTableName(table);
    }

    public HbaseUtil table(String t) {
        this.setTableName(t);
        return this;
    }

    public HbaseUtil family(String f) {
        this.setFamilyName(f);
        return this;
    }

    public HbaseUtil columns(List<String> f) {
        this.setColumns(f);
        return this;
    }

    public HbaseUtil(String table, String family) {
        setConnection();
        this.setFamilyName(family);
        this.setTableName(table);
    }

    public HbaseUtil(String table, String family, List<String> columns) {
        setConnection();
        this.setFamilyName(family);
        this.setTableName(table);
        this.setColumns(columns);
    }

    private void setConnection() {
        try {
            this.connection = ConnectionFactory.createConnection(config);
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public void setFamilyName(String f) {
        this.familyName = f;
    }

    public void setTableName(String t) {
        this.tableName = t;
    }

    public void setColumns(String... cs) {
        this.columns = new ArrayList<String>();
        for (String c : cs)
            this.columns.add(c);
//        System.out.println("set columns");
    }

    public void setColumns(List<String> cs) {
        this.columns = new ArrayList<String>();
        for (String c : cs)
            this.columns.add(c);
//        System.out.println("set columns");
    }

    public void setFields(List<String> fs) {
        this.fields = new ArrayList<String>();
        for (String f : fs)
            this.fields.add(f);
//        System.out.println("set fields");
    }

    public void close() {
        try {
            if (null != connection)
                this.connection.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static byte[] Trans(String raw) {
        return Bytes.toBytes(raw);
    }

    public static String Trans(byte[] raw) {
        return Bytes.toString(raw);
    }

    private String generateRowKey() {
        if (null != this.fields) {
            String rowKey = "";
            for (String field : this.fields) {
                rowKey += field;
                rowKey += "_";
            }
            rowKey += UUID.randomUUID().toString().substring(24);
            return rowKey;
        } else {
            System.out.println("Need To Set Fields !!!");
            return null;
        }
    }

    public static String generateRowKey(List<String> fields) {
        String rowKey = "";
        for (String field : fields) {
            rowKey += field;
            rowKey += "_";
        }
        rowKey += UUID.randomUUID().toString().substring(24);
        return rowKey;
    }


    /**
     * @param tableName
     * @param family
     * @param rowKey
     * @param column
     * @param value
     */
    public void replaceInsert(String tableName, String family, String rowKey, List<String> column, List<String> value) {
        try {
            Table table = this.connection.getTable(TableName.valueOf(tableName));
            Put put = new Put(Trans(rowKey));
            int columnSize = column.size();
            for (int i = 0; i < columnSize; i++)
                put.addColumn(Trans(family), Trans(column.get(i)), Trans(value.get(i)));
            table.put(put);

            table.close();
            System.out.println("Insert Cell "+rowKey);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * @param tableName
     * @param family
     * @param rowKeys
     * @param column
     * @param values
     */
    public void replaceInsert(String tableName, String family, List<String> rowKeys, List<String> column, List<List<String>> values) {
        try {
            Table table = this.connection.getTable(TableName.valueOf(tableName));
            List<Put> putList = new ArrayList<Put>();
            int columnSize = column.size();
            int i = 0;
            for (List<String> value : values) {
                Put put = new Put(Trans(rowKeys.get(i++)));
                for (int j = 0; j < columnSize; ++j) {
                    put.addColumn(Trans(family), Trans(column.get(j)), Trans(value.get(j)));
                }
                putList.add(put);
            }
            table.put(putList);
            table.close();
//            System.out.println("insert success");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * @param rowKey
     * @param value
     */
    public void replaceInsert(String rowKey, List<String> value) {
        if (null != this.tableName && null != this.familyName && null != this.columns)
            try {
                Table table = this.connection.getTable(TableName.valueOf(this.tableName));
                Put put = new Put(Trans(rowKey));
//                System.out.println(rowKey);
                int columnSize = this.columns.size();
                for (int i = 0; i < columnSize; i++){

//                    System.out.println(this.columns.get(i));
//                    System.out.println(value.get(i));
                    put.addColumn(Trans(this.familyName), Trans(this.columns.get(i)), Trans(value.get(i)));
                }

                table.put(put);
                table.close();
//                System.out.println("Insert Cell");
            } catch (Exception e) {
                e.printStackTrace();
            }
        else {
            System.out.println("Need To Set tableName, familyName, columns !!!");
        }
    }

    /**
     * @param rowKeys
     * @param values
     */
    public void replaceInsert(List<String> rowKeys, ArrayList<ArrayList<String>> values) {
        if (null != this.tableName && null != this.familyName && null != this.columns)
            try {
                Table table = this.connection.getTable(TableName.valueOf(this.tableName));
                List<Put> putList = new ArrayList<Put>();
                int columnSize = this.columns.size();
                int i = 0;
                for (List<String> value : values) {
                    Put put = new Put(Trans(rowKeys.get(i++)));
                    for (int j = 0; j < columnSize; ++j) {
                        put.addColumn(Trans(this.familyName), Trans(this.columns.get(j)), Trans(value.get(j)));
                    }
                    putList.add(put);
                }
                table.put(putList);
                table.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        else {
            System.out.println("Need To Set tableName, familyName, columns !!!");
        }
    }

    /**
     * @param table
     * @param familys
     */
    public void createTable(String table, List<String> familys) {
        try {
            Admin admin = connection.getAdmin();
            if (admin.tableExists(TableName.valueOf(table))) {
                System.out.println("FATAL ERROR: TABLE EXIST!");
            } else {
                HTableDescriptor dscrpt = new HTableDescriptor(TableName.valueOf(table));
                for (String f : familys)
                    dscrpt.addFamily(new HColumnDescriptor(f));
                admin.createTable(dscrpt);
                System.out.println("Create Table: " + table);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     *
     QualifierFilter
     用于列名（Qualifier）过滤。
     Scan scan = new Scan();
     QualifierFilter filter = new QualifierFilter(CompareOp.EQUAL, new BinaryComparator(Bytes.toBytes("my-column"))); // 列名为 my-column
     scan.setFilter(filter);
     */

    /**
     * @param tableName
     * @param rowKey
     * @return
     */
    public Result query(String tableName, String rowKey) {
        try {
            Get get = new Get(Trans(rowKey));
            Table table = this.connection.getTable(TableName.valueOf(tableName));// 获取表
            Result result = table.get(get);
            table.close();
            return result;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * @param tableName
     * @param startRowKey
     * @param stopRowKey
     * @return
     */
    public ResultScanner query(String tableName, String startRowKey, String stopRowKey) {
        try {
            Table table = this.connection.getTable(TableName.valueOf(tableName));// 获取表
            Scan scan = new Scan();
            scan.setStartRow(Trans(startRowKey));
            scan.setStopRow(Trans(stopRowKey));
            ResultScanner rs = table.getScanner(scan);
            table.close();
            return rs;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * @param tableName
     * @param startRowKey
     * @param stopRowKey
     * @param selectFml
     * @param selectCols
     * @return
     */
    public ResultScanner query(String tableName, String startRowKey, String stopRowKey, String selectFml, String... selectCols) {
        try {
            Table table = this.connection.getTable(TableName.valueOf(tableName));// 获取表
            Scan scan = new Scan();
            scan.setStartRow(Trans(startRowKey));
            scan.setStopRow(Trans(stopRowKey));
            for (String col : selectCols)
                scan.addColumn(Trans(selectFml), Trans(col));
            ResultScanner rs = table.getScanner(scan);
            table.close();
            return rs;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * @param tableName
     * @param startRowKey
     * @param stopRowKey
     * @param selectFml
     * @param selectCols
     * @return
     */
    public ResultScanner query(String tableName, String startRowKey, String stopRowKey, String selectFml, List<String> selectCols) {
        try {
            Table table = this.connection.getTable(TableName.valueOf(tableName));// 获取表
            Scan scan = new Scan();
            scan.setStartRow(Trans(startRowKey));
            scan.setStopRow(Trans(stopRowKey));
            for (String col : selectCols)
                scan.addColumn(Trans(selectFml), Trans(col));
            ResultScanner rs = table.getScanner(scan);
            table.close();
            return rs;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * @param tableName
     * @param rowKeys
     * @return
     */
    public Result[] query(String tableName, List<String> rowKeys) {
        try {
            Table table = this.connection.getTable(TableName.valueOf(tableName));// 获取表
            List<Get> gets = new ArrayList<Get>();
            for (String rowKey : rowKeys)
                gets.add(new Get(Trans(rowKey)));
            Result[] results = table.get(gets);
            table.close();
            return results;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * @param result
     */
    public static void print(Result result) {
        List<Cell> cells = result.listCells();
        for (Cell cell : cells) {
            System.out.println("rowKey: " + Trans(CellUtil.cloneRow(cell)));
            System.out.println("family:" + Trans(CellUtil.cloneFamily(cell)));
            System.out.println("qualifier:" + Trans(CellUtil.cloneQualifier(cell)));
            System.out.println("value:" + Trans(CellUtil.cloneValue(cell)));
            System.out.println("Timestamp:" + cell.getTimestamp());
            System.out.println("-------------------------------------------");
        }
    }

    /**
     * @param rs
     */
    public static void print(ResultScanner rs) {
        for (Result result : rs)
            print(result);
    }

    /**
     * @param results
     */
    public static void print(Result[] results) {
        for (Result result : results)
            print(result);
    }

    /**
     * rowkey的例子，需要自己定义！！！！！！
     *
     * @param fields
     * @return
     */
    private String makeRowKey(String... fields) {
        String ret = "bc";
        for (String field : fields) {
            ret += field;
            ret += "_";
        }
        ret = ret.substring(0, ret.length() - 1);
        ret += UUID.randomUUID().toString().substring(24);
        return ret;
    }

    /**
     * 列的设置，需要自己定义！！！！！！
     *
     * @return
     */
    public static List<String> makeColumns() {
        List<String> columns = new ArrayList<String>();
        columns.add("username");
        columns.add("repostnum");
        columns.add("commentnum");
        columns.add("likenum");
        columns.add("posttime");
        columns.add("content");
        return columns;
    }

    /**
     * 一行值的设置，需要自己定义！！！！！！
     *
     * @param raw
     * @return
     */
    public static List<String> makeValues(List raw) {
        List<String> values = new ArrayList<String>();
        values.add(String.valueOf(raw.get(1)));
        values.add(String.valueOf(raw.get(3)));
        values.add(String.valueOf(raw.get(4)));
        values.add(String.valueOf(raw.get(5)));
        values.add("-1");
        values.add(String.valueOf(raw.get(7)));
        return values;
    }

    public static void main(String[] args) {
        HbaseUtil hbase = new HbaseUtil()
                .table("forecast")
                .family("weibo");
//        ArrayList<String> family = new ArrayList<String>();
//        family.add("TwitterDAO");
//        family.add("weibo");
//        hbase.createTable("timzxz", family);
//        ArrayList<String> columns = new ArrayList<String>();
//        columns.add("nrepost");
//        columns.add("nlike");
//        columns.add("ncomment");
//
//        ArrayList<String> value = new ArrayList<String>();
//        value.add("sdsdfwe");
//        value.add("fdsfsfwe");
//        value.add("sagFDuioherg");
//
//        String rowKey = "testcell24";
//        hbase.replaceInsert("timzxz", "Twitter", rowKey, columns, value);
//
//        ArrayList<String> rowkeys = new ArrayList<String>();
//        rowkeys.add("123464");
//        rowkeys.add("123465");
//        ArrayList<String> value1 = new ArrayList<String>();
//        value1.add("uiahgei");
//        value1.add("df356sdg");
//        value1.add("dgfh25454");
//        ArrayList<String> value2 = new ArrayList<String>();
//        value2.add("547sighi");
//        value2.add("541efw15");
//        value2.add("timzxzzz");
//
//        List<List<String>> values = new ArrayList<List<String>>();
//        values.add(value1);
//        values.add(value2);
//        hbase.replaceInsert("timzxz", "TwitterDAO", rowkeys, columns, values);
        print(hbase.query("forecast", "ba101772207^", "ba101772207`"));
//        print(hbase.query("timzxz", "123456", "123465"));
        hbase.close();/* 用完记得close */
    }

}