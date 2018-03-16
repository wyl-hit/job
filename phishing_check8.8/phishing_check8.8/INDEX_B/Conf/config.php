<?php
return array(
	// 添加数据库配置信息
'DB_TYPE'   => 'mysql', // 数据库类型
//'DB_HOST'   => 'localhost',//本机数据库
'DB_HOST'   => '192.168.65.148', // 服务器地址
'DB_NAME'   => 'phishing_check', // 数据库名
'DB_USER'   => 'root', // 用户名
'DB_PWD'    => '', // 密码
'DB_PORT'   => 3306, // 端口
'DB_PREFIX' => '', // 数据库表前缀

//数据库类型：//数据库地址：数据库端口/数据库名
'DB_MONGO' =>'mongodb://192.168.65.148:27017/phishing_check',
//图片地址前缀
'ADDRESS_PRE' => 'http://192.168.174.128',
//图片地址被替换字段
'BREPLACE' => 'gray_web',
'AMRPLACE' => 'monitor_web',
//图片地址替换字段
'AREPLACE' => 'counterfeit_web',

//系统日志
//用户管理
'ACTION_LOGIN' =>'login in the system ',//登录系统
'ACTION_OPTLOG'   =>'output the userlog ',//导出用户日志
'ACTION_DELOG'   => 'empty the userlog',//清空用户日志
//白名单管理

'ACTION_ADDPL' =>'input the protected websites ',//导入白名单
'ACTION_ADDTL' =>'input the trusted websites ',//导入被信任网站名单
'ACTION_DELPL' =>'delete the protected websites ',//删除白名单
'ACTION_DELTL' =>'delete the trusted websites ',//删除白名单
'ACTION_OPTPLIST' =>'output the protected websites ',//导出白名单
'ACTION_OPTTLIST' =>'output the trusted websites ',//导出白名单
//可疑名单管理
'ACTION_DLSLIST' =>'download the suspected websites ',//下载可疑名单
'ACTION_ADDSLIST' =>'input the suspected websites ',//导入可疑名单
'ACTION_RUNSLIST' =>'run the corresponding task',//再次运行对应任务
//任务管理
'ACTION_ADDTASK' =>'add a new task ',//添加新任务
'ACTION_STARTTASK' =>'start a task ',//启动任务
'ACTION_TASKSTATE' =>'check the task state',//查看任务状态
'ACTION_TASKRESULT' =>'check the task result ',//查看任务结果
'ACTION_STOPTASK'   =>'stop the task ',//终止任务
'ACTION_DELTASK' =>'delete the task ',//删除任务
//系统配置
'ACTION_ADDUCH' =>'input new url change rules ',//添加域名变换规则
'ACTION_ADDKW' =>'input new key words ',//添加敏感词
'ACTION_DELUCH' =>'delete change rules ',//删除域名变换规则
'ACTION_DELKW' =>'delete sensitive key words ',//删除敏感词
'ACTION_OPTUCH' =>'output change rules ',//删除域名变换规则
'ACTION_OPTKW' =>'output sensitive key words ',//删除敏感词

);
?>
