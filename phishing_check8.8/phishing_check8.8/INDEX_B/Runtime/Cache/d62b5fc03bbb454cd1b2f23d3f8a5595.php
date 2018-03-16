<?php if (!defined('THINK_PATH')) exit();?><!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
  <meta name="description" content="">
  <meta name="author" content="ThemeBucket">
  <link rel="shortcut icon" href="#" type="image/png">

  <title>任务结果 </title>

  <!--data table-->
  <link href="__TMPL__/js/advanced-datatable/css/demo_page.css" rel="stylesheet" />
  <link href="__TMPL__/js/advanced-datatable/css/demo_table.css" rel="stylesheet" />
  <link rel="stylesheet" href="__TMPL__/js/data-tables/DT_bootstrap.css" />

  <link href="__TMPL__/css/style.css" rel="stylesheet">
  <link rel="stylesheet" href="__TMPL__/css/style_time.css" media="screen" type="text/css" />
  <link href="__TMPL__/css/style-responsive.css" rel="stylesheet">

  <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
  <!--[if lt IE 9]>
  <script src="js/html5shiv.js"></script>
  <script src="js/respond.min.js"></script>
  <![endif]-->
</head>

<body class="sticky-header">

<section>
    <!-- left side start-->
    <div class="left-side sticky-left-side">

        <!--logo and iconic logo start-->
        <div class="logo">
            <a href="__APP__/Index/indexMain.html"><img src="__TMPL__/images/logo.png" alt=""></a>
        </div>

        <div class="logo-icon text-center">
            <a href="__APP__/Index/indexMain.html"><img src="__TMPL__/images/logo_icon.png" alt=""></a>
        </div>
        <!--logo and iconic logo end-->


        <div class="left-side-inner">

            <!-- visible to small devices only -->
            <div class="visible-xs hidden-sm hidden-md hidden-lg">
                <div class="media logged-user">
                    <img alt="" src="images/photos/user-avatar.png" class="media-object">
                    <div class="media-body">
                        <h4><a href="#">John Doe</a></h4>
                        <span>"Hello There..."</span>
                    </div>
                </div>

                <h5 class="left-nav-title">Account Information</h5>
                <ul class="nav nav-pills nav-stacked custom-nav">
                    <li><a href="#"><i class="fa fa-user"></i> <span>Profile</span></a></li>
                    <li><a href="#"><i class="fa fa-cog"></i> <span>Settings</span></a></li>
                    <li><a href="#"><i class="fa fa-sign-out"></i> <span>Sign Out</span></a></li>
                </ul>
            </div>

             <!--sidebar nav start-->
            <ul class="nav nav-pills nav-stacked custom-nav">
                 <li><a href="__APP__/Index/indexMain.html"><i class="fa fa-bullhorn"></i> <span>首页</span></a></li>

                <li class="menu-list"><a href=""><i class="fa fa-book"></i> <span>白名单管理</span></a>
                    <ul class="sub-menu-list">
                       <li><a href="__APP__/Wlist/wlist_index.html"> 查看被保护网站名单</a></li>
                        <li><a href="__APP__/Wlist/wlist_trusted.html"> 查看被信任网站名单</a></li>
                        <li><a href="__APP__/Wlist/wlist_add.html"> 添加白名单</a></li>
                       

                    </ul>
                </li>
                  <li class="menu-list"><a href=""><i class="fa fa-laptop"></i> <span>可疑名单管理</span></a>
                    <ul class="sub-menu-list">
                        <li><a href="__APP__/Slist/slist_index.html"> 查看可疑名单</a></li>
                         <li ><a href="__APP__/Slist/monitor.html"> 查看重点监测名单</a></li>
                        <li><a href="__APP__/Slist/slist_add.html"> 添加可疑名单</a></li>
                       

                    </ul>
                </li>
                 <li class="menu-list"><a href=""><i class="fa fa-bullhorn"></i> <span>黑名单管理</span></a>
                    <ul class="sub-menu-list">
                     <li><a href="__APP__/Blist/blist_add.html"> 添加黑名单</a></li>
                        <li ><a href="__APP__/Blist/index.html"> 查看黑名单</a></li>
                        <li><a href="__APP__/Blist/blist_source.html"> 查看被仿冒网站</a></li>
                         <li ><a href="__APP__/Blist/blist_model.html"> 查看仿冒网站模板</a></li>
                          <li ><a href="__APP__/Blist/whois_index.html"> 查看仿冒网站whois信息</a></li>
                         <li><a href="__APP__/Blist/whois_contact.html"> 查看仿冒网站注册人信息</a></li>
                         <li ><a href="__APP__/Blist/whois_domain.html"> 查看whois反查域名</a></li>
                        

                       

                    </ul>
                </li>
                

             
                  <li class="menu-list nav-active"><a href=""><i class="fa fa-cogs"></i> <span>任务管理</span></a>
              
                    <ul class="sub-menu-list">
                         <li ><a href="__APP__/Task/task_index.html"> 查看任务</a></li>
                        <li><a href="__APP__/Task/task_add.html"> 添加任务</a></li>
                        
                        <li class="active"><a href="__APP__/Task/task_result.html"> 查看任务状态</a></li>
                    </ul>
                </li>
            <li class="menu-list"><a href=""><i class="fa fa-book"></i> <span>系统配置</span></a>
                    <ul class="sub-menu-list">
                        <li><a href="__APP__/Config/addConfig.html"> 添加配置信息</a></li>
                       <li><a href="__APP__/Config/url_change.html">域名变换规则设置</a></li>
                        <li><a href="__APP__/Config/keyword.html"> 敏感关键字设置</a></li>
                       

                    </ul>
                </li>
               <li><a href="__APP__/User/user_index.html"><i class="fa fa-bullhorn"></i> <span>用户管理</span></a></li>
                
            <!--sidebar nav end-->

        </div>
    </div>
    <!-- left side end-->
    
    <!-- main content start-->
    <div class="main-content" >

        <!-- header section start-->
        <div class="header-section">

        <!--toggle button start-->
        <a class="toggle-btn"><i class="fa fa-bars"></i></a>
        <!--toggle button end-->

        <!--search start-->
        <form class="searchform" action="http://view.jqueryfuns.com/2014/4/10/7_df25ceea231ba5f44f0fc060c943cdae/indexMain.html" method="post">
            <input type="text" class="form-control" name="keyword" placeholder="Search here..." />
        </form>
        <!--search end-->

        <!--notification menu start -->
        <div class="menu-right">
            <ul class="notification-menu">
                <li>
                    <a href="#" class="btn btn-default dropdown-toggle info-number" data-toggle="dropdown">
                        <i class="fa fa-tasks"></i>
                        <span class="badge">8</span>
                    </a>
                    <div class="dropdown-menu dropdown-menu-head pull-right">
                        <h5 class="title">You have 8 pending task</h5>
                        <ul class="dropdown-list user-list">
                            <li class="new">
                                <a href="#">
                                    <div class="task-info">
                                        <div>Database update</div>
                                    </div>
                                    <div class="progress progress-striped">
                                        <div style="width: 40%" aria-valuemax="100" aria-valuemin="0" aria-valuenow="40" role="progressbar" class="progress-bar progress-bar-warning">
                                            <span class="">40%</span>
                                        </div>
                                    </div>
                                </a>
                            </li>
                            <li class="new">
                                <a href="#">
                                    <div class="task-info">
                                        <div>Dashboard done</div>
                                    </div>
                                    <div class="progress progress-striped">
                                        <div style="width: 90%" aria-valuemax="100" aria-valuemin="0" aria-valuenow="90" role="progressbar" class="progress-bar progress-bar-success">
                                            <span class="">90%</span>
                                        </div>
                                    </div>
                                </a>
                            </li>
                            <li>
                                <a href="#">
                                    <div class="task-info">
                                        <div>Web Development</div>
                                    </div>
                                    <div class="progress progress-striped">
                                        <div style="width: 66%" aria-valuemax="100" aria-valuemin="0" aria-valuenow="66" role="progressbar" class="progress-bar progress-bar-info">
                                            <span class="">66% </span>
                                        </div>
                                    </div>
                                </a>
                            </li>
                            <li>
                                <a href="#">
                                    <div class="task-info">
                                        <div>Mobile App</div>
                                    </div>
                                    <div class="progress progress-striped">
                                        <div style="width: 33%" aria-valuemax="100" aria-valuemin="0" aria-valuenow="33" role="progressbar" class="progress-bar progress-bar-danger">
                                            <span class="">33% </span>
                                        </div>
                                    </div>
                                </a>
                            </li>
                            <li>
                                <a href="#">
                                    <div class="task-info">
                                        <div>Issues fixed</div>
                                    </div>
                                    <div class="progress progress-striped">
                                        <div style="width: 80%" aria-valuemax="100" aria-valuemin="0" aria-valuenow="80" role="progressbar" class="progress-bar">
                                            <span class="">80% </span>
                                        </div>
                                    </div>
                                </a>
                            </li>
                            <li class="new"><a href="">See All Pending Task</a></li>
                        </ul>
                    </div>
                </li>
                <li>
                    <a href="#" class="btn btn-default dropdown-toggle info-number" data-toggle="dropdown">
                        <i class="fa fa-envelope-o"></i>
                        <span class="badge">5</span>
                    </a>
                    <div class="dropdown-menu dropdown-menu-head pull-right">
                        <h5 class="title">You have 5 Mails </h5>
                        <ul class="dropdown-list normal-list">
                            <li class="new">
                                <a href="">
                                    <span class="thumb"><img src="images/photos/user1.png" alt="" /></span>
                                        <span class="desc">
                                          <span class="name">John Doe <span class="badge badge-success">new</span></span>
                                          <span class="msg">Lorem ipsum dolor sit amet...</span>
                                        </span>
                                </a>
                            </li>
                            <li>
                                <a href="">
                                    <span class="thumb"><img src="images/photos/user2.png" alt="" /></span>
                                        <span class="desc">
                                          <span class="name">Jonathan Smith</span>
                                          <span class="msg">Lorem ipsum dolor sit amet...</span>
                                        </span>
                                </a>
                            </li>
                            <li>
                                <a href="">
                                    <span class="thumb"><img src="images/photos/user3.png" alt="" /></span>
                                        <span class="desc">
                                          <span class="name">Jane Doe</span>
                                          <span class="msg">Lorem ipsum dolor sit amet...</span>
                                        </span>
                                </a>
                            </li>
                            <li>
                                <a href="">
                                    <span class="thumb"><img src="images/photos/user4.png" alt="" /></span>
                                        <span class="desc">
                                          <span class="name">Mark Henry</span>
                                          <span class="msg">Lorem ipsum dolor sit amet...</span>
                                        </span>
                                </a>
                            </li>
                            <li>
                                <a href="">
                                    <span class="thumb"><img src="images/photos/user5.png" alt="" /></span>
                                        <span class="desc">
                                          <span class="name">Jim Doe</span>
                                          <span class="msg">Lorem ipsum dolor sit amet...</span>
                                        </span>
                                </a>
                            </li>
                            <li class="new"><a href="">Read All Mails</a></li>
                        </ul>
                    </div>
                </li>
                <li>
                    <a href="#" class="btn btn-default dropdown-toggle info-number" data-toggle="dropdown">
                        <i class="fa fa-bell-o"></i>
                        <span class="badge">4</span>
                    </a>
                    <div class="dropdown-menu dropdown-menu-head pull-right">
                        <h5 class="title">Notifications</h5>
                        <ul class="dropdown-list normal-list">
                            <li class="new">
                                <a href="">
                                    <span class="label label-danger"><i class="fa fa-bolt"></i></span>
                                    <span class="name">Server #1 overloaded.  </span>
                                    <em class="small">34 mins</em>
                                </a>
                            </li>
                            <li class="new">
                                <a href="">
                                    <span class="label label-danger"><i class="fa fa-bolt"></i></span>
                                    <span class="name">Server #3 overloaded.  </span>
                                    <em class="small">1 hrs</em>
                                </a>
                            </li>
                            <li class="new">
                                <a href="">
                                    <span class="label label-danger"><i class="fa fa-bolt"></i></span>
                                    <span class="name">Server #5 overloaded.  </span>
                                    <em class="small">4 hrs</em>
                                </a>
                            </li>
                            <li class="new">
                                <a href="">
                                    <span class="label label-danger"><i class="fa fa-bolt"></i></span>
                                    <span class="name">Server #31 overloaded.  </span>
                                    <em class="small">4 hrs</em>
                                </a>
                            </li>
                            <li class="new"><a href="">See All Notifications</a></li>
                        </ul>
                    </div>
                </li>
                <li>
                    <a href="#" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                        <img src="images/photos/user-avatar.png" alt="" />
                        John Doe
                        <span class="caret"></span>
                    </a>
                    <ul class="dropdown-menu dropdown-menu-usermenu pull-right">
                        <li><a href="#"><i class="fa fa-user"></i>  Profile</a></li>
                        <li><a href="#"><i class="fa fa-cog"></i>  Settings</a></li>
                        <li><a href="#"><i class="fa fa-sign-out"></i> Log Out</a></li>
                    </ul>
                </li>

            </ul>
        </div>
        <!--notification menu end -->

        </div>
        <!-- header section end-->

        <!-- page heading start-->
        <div class="page-heading">
            <h3>
              
            </h3>
            <ul class="breadcrumb">
                 <li><a href="__APP__/Index/indexMain.html">首页</a></li>
				
                <li>
                    <a href="#">任务管理</a>
                </li>
                <li class="active"> 查看任务结果 </li>
            </ul>
        </div>
        <!-- page heading end-->

        <!--body wrapper start-->
        <div class="wrapper">

            <div class="row">
                <div class="col-md-12">

                    <section class="panel">
                        <header class="panel-heading custom-tab ">
                            <ul class="nav nav-tabs">
                                <li class="active">
                                    <a href="#home" class="change" data-toggle="tab">正在进行中的任务</a>
                                </li>
                                <li class="">
                                    <a href="#about" class="change" data-toggle="tab">已完成的任务</a>
                                </li>
                                <li >
                                    <a href="#contact" class="change" data-toggle="tab">失败的任务</a>
                                </li>
                               
                            </ul>
                        </header>
                        <div class="panel-body">
                            <div class="tab-content">
                                <div class="tab-pane active" id="home">
                                     <table class="table">
                            <thead>
                            <tr>
                                
                                
                                <th>当前运行任务编号</th>
                                <th>当前运行任务名称</th>
                                <th>任务类型</th>
                                <th>开始时间</th>
                                
                                <th>操作</th>
                               
                            </tr>
                            </thead>
                            <tbody>
                                <?php if(is_array($taskinfo)): $i = 0; $__LIST__ = $taskinfo;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                   <th class="taskid" id="<?php echo ($one["id"]); ?>"><?php echo ($one["id"]); ?></th>
                                    <th><?php echo ($one["name"]); ?></th>
                                    
                                    <th><?php if(($one["type"] == 1)): ?>探测任务
                                        <?php else: ?>探测及验证任务<?php endif; ?>
                                    </th>

                                    <th class= "starttime" id="<?php echo ($one["time"]); ?>"><?php echo ($one["time"]); ?></th>
                                    
                                  
                                   
                                    
                                    <th>
                                        <a href="#" class="btn  btn-primary btn-info btn-xs view_stop" id = "<?php echo ($one["id"]); ?>">停止</a>
                                        <a href="#"  class="btn btn-primary btn-info btn-xs view_process" >查看</a>
                                    </th>
                                </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                            </tbody>
                        </table>
                                    
                                </div>
                                <div class="tab-pane" id="about">
                                           <table  class="display table table-bordered table-striped" id="dynamic-table">
                                                <thead>
                                                <tr>
                                                    <th>任务id</th>
                                                    <th>启动时间</th>
                                                    <th>任务用时</th>
                                                    <th>任务类型</th>
                                                    <th>结果查看</th>
                                                </tr>
                                                </thead>

                                                <tbody>
                                                    <?php if(is_array($task)): $i = 0; $__LIST__ = $task;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr class="">
                                                        <td id ="<?php echo ($one["task_id"]); ?>"><?php echo ($one["task_id"]); ?></td>
                                                        <td id = "<?php echo ($one["start_time"]); ?>"><?php echo ($one["start_time"]); ?></td>
                                                        <td><?php echo ($one["run_time"]); ?></td>
                                                        <td><?php if(($one["task_type"] == 1)): ?>探测任务  
                                                            <?php else: ?>探测及验证任务<?php endif; ?></td></td>
                                                        
                                                        <th><a href="#" class= "btn btn-primary btn-info btn-xs  view_result">查看</a></th>
                                                        
                                                       
                                                    </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                                                </tbody>
                                            </table>
                                    
                                </div>
                                 <div class="tab-pane" id="contact">
                                    <table class="table">
                                                <thead>
                                                <tr>
                                                    <th>任务id</th>
                                                    <th>启动时间</th>
                                                    <th>任务用时</th>
                                                    <th>任务类型</th>
                                                    <th>结果查看</th>
                                                </tr>
                                                </thead>

                                                <tbody>
                                                    <?php if(is_array($task_fail)): $i = 0; $__LIST__ = $task_fail;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr class="">
                                                        <td id ="<?php echo ($one["task_id"]); ?>"><?php echo ($one["task_id"]); ?></td>
                                                        <td id = "<?php echo ($one["start_time"]); ?>"><?php echo ($one["start_time"]); ?></td>
                                                        <td><?php echo ($one["run_time"]); ?></td>
                                                        <td><?php if(($one["task_type"] == 1)): ?>探测任务  
                                                            <?php else: ?>探测及验证任务<?php endif; ?></td></td>
                                                        
                                                        <th><a href="#" class= "btn btn-primary btn-info btn-xs  view_result">查看</a></th>
                                                        
                                                       
                                                    </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                                                </tbody>
                                            </table>
                                    
                                </div>
                                
                            </div>
                        </div>
                    </section>

                  
                </div>
                
            </div>
            <div class="row">
                <div class="col-sm-6" id="whois_state">
                        <section class="panel">
                             <header class="panel-heading">
                                whois探测引擎结果
                                <span class="tools pull-right">
                                <a href="javascript:;" class="fa fa-chevron-down"></a>
                                <a href="javascript:;" class="fa fa-times"></a>
                                </span>
                            </header>
                            <div class="panel-body">
                                <table class="table table-striped table-hover table-bordered" >
                                    <thead>
                                    <tr>
                                        <th>状态</th>
                                        <th>执行时间</th>
                                        
                                    </tr>
                                    </thead>
                                    <tbody id="zero">
                                    <?php if(is_array($result)): $i = 0; $__LIST__ = $result;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                       
                                        <th id="state"></th>
                                        <th id= "time"></th>
                                    </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                                    </tbody>
                                </table>
                            </div>
                        </section>
                </div>
                <div class="col-sm-6" id="domain_state">
                        <section class="panel">
                             <header class="panel-heading">
                                域名变换探测引擎结果
                                <span class="tools pull-right">
                                <a href="javascript:;" class="fa fa-chevron-down"></a>
                                <a href="javascript:;" class="fa fa-times"></a>
                                </span>
                            </header>
                            <div class="panel-body">
                                <table class="table table-striped table-hover table-bordered" >
                                    <thead>
                                    <tr>
                                        <th>状态</th>
                                        
                                        <th>生成域名总数</th>
                                        <th>生成域名存在数</th>
                                        <th>探测域名数</th>
                                        <th>生成可疑名单数</th>
                                        <th>运行时间</th>
                                        
                                    </tr>
                                    </thead>
                                    <tbody id="zero">
                                    <?php if(is_array($result)): $i = 0; $__LIST__ = $result;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                        <th id="state"></th>
                                        <th id="changed"></th>
                                        <th id="exist"></th>
                                        <th id="detected"></th>
                                        <th id="suspected"></th>
                                        <th id= "time"></th>
                                    </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                                    </tbody>
                                </table>
                            </div>
                        </section>
                </div>

                <div class="col-sm-6" id="filtrate_state">
                <section class="panel">
                    <header class="panel-heading">
                        灰名单过滤引擎结果
                            <span class="tools pull-right">
                                <a href="javascript:;" class="fa fa-chevron-down"></a>
                                <a href="javascript:;" class="fa fa-times"></a>
                             </span>
                    </header>
                    <div class="panel-body">
                        <table class="table table-striped table-hover table-bordered" >
                            <thead>
                            <tr>
                                <th>状态</th>
                                <th>被信任名单过滤数量</th>
                                <th>黑名单过滤数量</th>

                                <th>执行时间</th>
                                
                            </tr>
                            </thead>
                            <tbody id="zero">
                            <?php if(is_array($result)): $i = 0; $__LIST__ = $result;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                               
                              <th id="state"></th>
                                <th id="protected_filtrate"></th>
                                <th id="counterfeit_filtrate"></th>
                                
                               
                             
                                <th id="time"></th>
                               
                                
                              
                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                            </tbody>
                        </table>
                    </div>

                </section>
            </div>

            <div class="col-sm-6" id="web_save_state">
                <section class="panel">
                    <header class="panel-heading">
                        网页信息保存引擎结果
                            <span class="tools pull-right">
                                <a href="javascript:;" class="fa fa-chevron-down"></a>
                                <a href="javascript:;" class="fa fa-times"></a>
                             </span>
                    </header>
                    <div class="panel-body">
                        <table class="table table-striped table-hover table-bordered" >
                            <thead>
                            <tr>
                                <th>状态</th>
                                <th>请求数量</th>
                                <th>保存数量</th>
                                
                                <th>执行时间</th>
                                
                            </tr>
                            </thead>
                            <tbody id="zero">
                            <?php if(is_array($result)): $i = 0; $__LIST__ = $result;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                               <th id="state"></th>
                                 <th id="request"></th>
                                <th id="save"></th>
                                <th id = "time"></th>
 
                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                            </tbody>
                        </table>
                    </div>

                </section>
            </div>
             <div class="col-sm-6" id="feature_save_state">
                <section class="panel">
                    <header class="panel-heading">
                        特征保存引擎结果
                            <span class="tools pull-right">
                                <a href="javascript:;" class="fa fa-chevron-down"></a>
                                <a href="javascript:;" class="fa fa-times"></a>
                             </span>
                    </header>
                    <div class="panel-body">
                        <table class="table table-striped table-hover table-bordered" >
                            <thead>
                            <tr>
                                <th>状态</th>
                               
                                <th>保存数量</th>
                                
                                <th>执行时间</th>
                                
                            </tr>
                            </thead>
                            <tbody id="zero">
                            <?php if(is_array($result)): $i = 0; $__LIST__ = $result;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                               <th id="state"></th>
                                
                                <th id="save"></th>
                                <th id = "time"></th>
 
                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                            </tbody>
                        </table>
                    </div>

                </section>
            </div>

                <div class="col-sm-6"  id="search_state">
                <section class="panel">
                    <header class="panel-heading">
                        元搜索敏感信息引擎结果
                            <span class="tools pull-right">
                                <a href="javascript:;" class="fa fa-chevron-down"></a>
                                <a href="javascript:;" class="fa fa-times"></a>
                             </span>
                    </header>
                    <div class="panel-body">
                        <table class="table table-striped table-hover table-bordered">
                            <thead>
                            <tr>
                                
                                <th>搜索关键字数量</th>
                                <th>搜索到的URL数量</th>

                                
                                <th>执行时间</th>
                                
                            </tr>
                            </thead>
                            <tbody id="zero">
                            <?php if(is_array($result)): $i = 0; $__LIST__ = $result;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                               
                                 <th id="kword"></th>
                                <th id="url"></th>
                                <th id = "time"></th>
 
                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                            </tbody>
                        </table>
                    </div>

                </section>
            </div>

                <div class="col-sm-6" id="qt_state">
                <section class="panel">
                    <header class="panel-heading">
                        页面视觉块划分引擎结果
                            <span class="tools pull-right">
                                <a href="javascript:;" class="fa fa-chevron-down"></a>
                                <a href="javascript:;" class="fa fa-times"></a>
                             </span>
                    </header>
                    <div class="panel-body">
                        <table class="table table-striped table-hover table-bordered" 
                            <thead>
                            <tr>

                                <th>状态</th>
                                <th>QT已抽取完成的url数量</th>
                               
                                
                                <th>执行时间</th>
                                
                            </tr>
                            </thead>
                            <tbody id="zero">
                            <?php if(is_array($result)): $i = 0; $__LIST__ = $result;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                               <th id = "state"></th>
                                 <th id="qt_url"></th>
                                
                                <th id = "time"></th>

 
                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                            </tbody>
                        </table>
                    </div>

                </section>
            </div>
         
                <div class="col-sm-6"  id="title_state">
                <section class="panel">
                    <header class="panel-heading">
                       网页关键字比对引擎结果
                            <span class="tools pull-right">
                                <a href="javascript:;" class="fa fa-chevron-down"></a>
                                <a href="javascript:;" class="fa fa-times"></a>
                             </span>
                    </header>
                    <div class="panel-body">
                        <table class="table table-striped table-hover table-bordered">
                            <thead>
                            <tr>
                                
                                <th>状态</th>
                                <th>检出数量</th>
                                <th>发现数量</th>
                                
                                <th>执行时间</th>
                                
                            </tr>
                            </thead>
                            <tbody id="zero">
                            <?php if(is_array($result)): $i = 0; $__LIST__ = $result;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                <th id="state"></th>
                                 <th id="check"></th>
                                <th id="find"></th>
                                <th id= "time"></th>
 
                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                            </tbody>
                        </table>
                    </div>

                </section>
            </div>

            <div class="col-sm-6" id="pageblock_state">
                <section class="panel">
                    <header class="panel-heading">
                        网页结构比对引擎结果
                            <span class="tools pull-right">
                                <a href="javascript:;" class="fa fa-chevron-down"></a>
                                <a href="javascript:;" class="fa fa-times"></a>
                             </span>
                    </header>
                    <div class="panel-body">
                        <table class="table table-striped table-hover table-bordered" >
                            <thead>
                            <tr>
                                
                                <th>状态</th>
                                <th>检出数量</th>
                                <th>发现数量</th>
                                
                                <th>执行时间</th>
                                
                            </tr>
                            </thead>
                            <tbody id="zero">
                            <?php if(is_array($result)): $i = 0; $__LIST__ = $result;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                               
                                 <th id="state"></th>
                                 <th id="check"></th>
                                <th id="find"></th>
                                <th id= "time"></th>
 
                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                            </tbody>
                        </table>
                    </div>

                </section>
            </div>
            <div class="col-sm-6" id="view_state">
                <section class="panel">
                    <header class="panel-heading">
                        网页视觉比对引擎结果
                            <span class="tools pull-right">
                                <a href="javascript:;" class="fa fa-chevron-down"></a>
                                <a href="javascript:;" class="fa fa-times"></a>
                             </span>
                    </header>
                    <div class="panel-body">
                        <table class="table table-striped table-hover table-bordered" >
                            <thead>
                            <tr>
                                
                                <th>状态</th>
                                <th>检出数量</th>
                                <th>发现数量</th>
                                
                                <th>执行时间</th>
                                
                            </tr>
                            </thead>
                            <tbody id="zero">
                            <?php if(is_array($result)): $i = 0; $__LIST__ = $result;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                               
                                 <th id="state"></th>
                                 <th id="check"></th>
                                <th id="find"></th>
                                <th id= "time"></th>
 
                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                            </tbody>
                        </table>
                    </div>

                </section>
            </div>
            </div>
				 
        </div>
        <div class="l-wrapper"id = "waiting">

    <svg viewBox="0 0 120 120" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <g id="circle" class="g-circles g-circles--v1">
            <circle id="12" transform="translate(35, 16.698730) rotate(-30) translate(-35, -16.698730) " cx="35" cy="16.6987298" r="10"></circle>
            <circle id="11" transform="translate(16.698730, 35) rotate(-60) translate(-16.698730, -35) " cx="16.6987298" cy="35" r="10"></circle>
            <circle id="10" transform="translate(10, 60) rotate(-90) translate(-10, -60) " cx="10" cy="60" r="10"></circle>
            <circle id="9" transform="translate(16.698730, 85) rotate(-120) translate(-16.698730, -85) " cx="16.6987298" cy="85" r="10"></circle>
            <circle id="8" transform="translate(35, 103.301270) rotate(-150) translate(-35, -103.301270) " cx="35" cy="103.30127" r="10"></circle>
            <circle id="7" cx="60" cy="110" r="10"></circle>
            <circle id="6" transform="translate(85, 103.301270) rotate(-30) translate(-85, -103.301270) " cx="85" cy="103.30127" r="10"></circle>
            <circle id="5" transform="translate(103.301270, 85) rotate(-60) translate(-103.301270, -85) " cx="103.30127" cy="85" r="10"></circle>
            <circle id="4" transform="translate(110, 60) rotate(-90) translate(-110, -60) " cx="110" cy="60" r="10"></circle>
            <circle id="3" transform="translate(103.301270, 35) rotate(-120) translate(-103.301270, -35) " cx="103.30127" cy="35" r="10"></circle>
            <circle id="2" transform="translate(85, 16.698730) rotate(-150) translate(-85, -16.698730) " cx="85" cy="16.6987298" r="10"></circle>
            <circle id="1" cx="60" cy="10" r="10"></circle>
        </g>
        <use xlink:href="#circle" class="use"/>
    </svg>
    
    
    </svg>
</div>
        <!--body wrapper end-->

        <!--footer section start-->
        <footer>
            2014 &copy; AdminEx by ThemeBucket
        </footer>
        <!--footer section end-->


    </div>
    <!-- main content end-->
</section>

<!-- Placed js at the end of the document so the pages load faster -->
<script src="__TMPL__/js/jquery-1.10.2.min.js"></script>
<script src="__TMPL__/js/jquery-ui-1.9.2.custom.min.js"></script>
<script src="__TMPL__/js/jquery-migrate-1.2.1.min.js"></script>
<script src="__TMPL__/js/bootstrap.min.js"></script>
<script src="__TMPL__/js/modernizr.min.js"></script>

<script src="__TMPL__/js/jquery.nicescroll.js"></script>

<!--data table-->
<script type="text/javascript" src="__TMPL__/js/data-tables/jquery.dataTables.js"></script>
<script type="text/javascript" src="__TMPL__/js/data-tables/DT_bootstrap.js"></script>

<!--common scripts for all pages-->
<script src="__TMPL__/js/scripts.js"></script>
<script src="__TMPL__/js/dynamic_table_init.js"></script>
<!--script for editable table-->

<!--script for editable table-->
<script src="__TMPL__/js/editable-table.js"></script>

<!-- END JAVASCRIPTS -->
<script type="text/javascript">
    jQuery(document).ready(function() {
        EditableTable.init();
    });
    $(document).ready(function(){
        $('#waiting').hide();
        var flagLast=0;

        $('#domain_state').hide();
        $('#qt_state').hide();
        $('#search_state').hide();
        $('#filtrate_state').hide();
        $('#web_save_state').hide();
        $('#title_state').hide();
        $('#pageblock_state').hide();
        $('#whois_state').hide();
        $('#feature_save_state').hide();
        $('#view_state').hide();

        $(".change").on("click", function(e) {
                $('#domain_state').hide();
                $('#qt_state').hide();
                $('#search_state').hide();
                $('#filtrate_state').hide();
                $('#web_save_state').hide();
                $('#title_state').hide();
                $('#pageblock_state').hide();
                $('#whois_state').hide();
                $('#feature_save_state').hide();
                $('#view_state').hide();
        });

        $(".view_process").on("click", function(e) {
            var tasktime = $(this).parent().prev().attr("id"); 
            var ctask_id = $(this).parent().prev().prev().prev().prev().attr("id"); 
            
            $.ajax({
                    type: "post",
                    url: "__APP__/Task/checkProcess",
                    data:{
                        id   : ctask_id,
                        time : tasktime
                        },
                    dataType: "json",
                    success: function(msg){
                        if (msg.status == 1 ) {

                            $('#domain_state').hide();
                            $('#qt_state').hide();
                            $('#search_state').hide();
                            $('#filtrate_state').hide();
                            $('#web_save_state').hide();
                            $('#title_state').hide();
                            $('#pageblock_state').hide();
                            $('#whois_state').hide();
                            $('#feature_save_state').hide();
                            $('#view_state').hide();


                            var domain_state = msg.data['e_domain_state'];
                            var search_state = msg.data['e_search_state'];
                            var filtrate_state = msg.data['e_filtrate_state'];
                            var web_save_state = msg.data['e_web_save_state'];
                            var title_state = msg.data['e_title_state'];
                            var pageblock_state = msg.data['e_structure_state'];
                            var qt_state = msg.data['e_qt_crawler_state'];
                            var whois_search_state = msg.data['e_whois_search_state'];
                            var feature_save_state = msg.data['e_feature_save_state'];
                            var view_collect_state = msg.data['e_view_collect_state'];


                            
                            if(domain_state>1){
                                $('#domain_state').show();
                                $('#domain_state').find("#state").html('正在运行');
                                $('#domain_state').find("#suspected").html(msg.data['domain_gray_url_num']);
                                $('#domain_state').find("#detected").html(msg.data['domain_detected_num']);
                                $('#domain_state').find("#changed").html(msg.data['domain_changed_all_num']);
                                $('#domain_state').find("#exist").html(msg.data['domain_changed_exist_num']);
                                
                                $('#domain_state').find("#time").html(msg.data['domain_run_time']+'s');
                                
                            }
                            if(filtrate_state>1){
                                $('#filtrate_state').show();
                                $('#filtrate_state').find("#state").html('正在运行');
                                $('#filtrate_state').find("#protected_filtrate").html(msg.data['filtrate_trusted_num']);
                                $('#filtrate_state').find("#counterfeit_filtrate").html(msg.data['filtrate_counterfeit_num']);
                                
                                $('#filtrate_state').find("#time").html(msg.data['filtrate_run_time']+'s');
                                
                            }
                            if(qt_state>1){
                                $('#qt_state').show();
                                $('#qt_state').find("#state").html('正在运行');
                                
                                $('#qt_state').find("#qt_url").html(msg.data['qt_crawler_num']);
                                
                                $('#qt_state').find("#time").html(msg.data['qt_crawler_run_time']+'s');
                                
                            }
                            if(web_save_state>1){
                                $('#web_save_state').show();
                                $('#web_save_state').find("#state").html('正在运行');
                                $('#web_save_state').find("#request").html(msg.data['web_request_num']);
                                $('#web_save_state').find("#save").html(msg.data['web_save_num']);
                                
                                $('#web_save_state').find("#time").html(msg.data['web_save_run_time']+'s');
                                
                            }
                            if(feature_save_state>1){
                                $('#feature_save_state').show();
                                $('#feature_save_state').find("#state").html('正在运行');
                               
                                $('#feature_save_state').find("#save").html(msg.data['feature_save_num']);
                                
                                $('#feature_save_state').find("#time").html(msg.data['feature_save_run_time']+'s');
                                
                            }
                            if(search_state>1){
                                $('#search_state').show();
                                $('#search_state').find("#state").html('正在运行');
                                $('#search_state').find("#kword").html(msg.data['search_kword_num']);
                                $('#search_state').find("#url").html(msg.data['search_url_num']);
                                
                                $('#search_state').find("#time").html(msg.data['search_run_time']+'s');
                                

                            }
                            
                            if(title_state>1){
                                $('#title_state').show();
                                $('#title_state').find("#state").html('正在运行');
                                $('#title_state').find("#check").html(msg.data['title_check_num']);
                                $('#title_state').find("#find").html(msg.data['title_find_num']);
                                
                                $('#title_state').find("#time").html(msg.data['title_run_time']+
                                    's');
                                
                                
                            }
                            if(pageblock_state>1){
                                $('#pageblock_state').show();
                                $('#pageblock_state').find("#state").html('正在运行');
                                $('#pageblock_state').find("#check").html(msg.data['title_check_num']);
                                $('#pageblock_state').find("#find").html(msg.data['title_find_num']);
                                
                                $('#pageblock_state').find("#time").html(msg.data['title_run_time']+
                                    's');
                                
                                
                            }
                            if(view_collect_state>1){
                                $('#view_state').show();
                                $('#view_state').find("#state").html('正在运行');
                                $('#view_state').find("#check").html(msg.data['title_check_num']);
                                $('#view_state').find("#find").html(msg.data['title_find_num']);
                                
                                $('#view_state').find("#time").html(msg.data['title_run_time']+
                                    's');
                                
                                
                            }
                            
                            if(flagLast){
                                    clearInterval(flagLast);
                                    flagLast = setInterval(show,1000);
                                }   
                                else{
                                    flagLast = setInterval(show,1000); 
                                }
                            

                        };
                        if (msg.status == 0) {
                            
                            alert(msg.info);      
                        }; 
                          
                    } 
            });
           
           
            
            function show(){
                $.ajax({
                    type: "post",
                    url: "__APP__/Task/checkProcess",
                    data:{
                        id   : ctask_id,
                        time : tasktime
                        },
                    dataType: "json",
                    success: function(msg){
                        if (msg.status == 1 ) {
                            var domain_state = msg.data['e_domain_state'];
                            var search_state = msg.data['e_search_state'];
                            var filtrate_state = msg.data['e_filtrate_state'];
                            var web_save_state = msg.data['e_web_save_state'];
                            var title_state = msg.data['e_title_state'];
                            var pageblock_state = msg.data['e_structure_state'];
                            var qt_state = msg.data['e_qt_crawler_state'];
                            var whois_search_state = msg.data['e_whois_search_state'];
                            var feature_save_state = msg.data['e_feature_save_state'];
                            var view_collect_state = msg.data['e_view_collect_state'];



                            
                            
                            if(domain_state==2){
                                 $('#domain_state').show();
                                $('#domain_state').find("#state").html('正在运行');
                                $('#domain_state').find("#suspected").html(msg.data['domain_gray_url_num']);
                                $('#domain_state').find("#detected").html(msg.data['domain_detected_num']);
                                $('#domain_state').find("#changed").html(msg.data['domain_changed_all_num']);
                                $('#domain_state').find("#exist").html(msg.data['domain_changed_exist_num']);
                                
                                $('#domain_state').find("#time").html(msg.data['domain_run_time']+'s');
                                
                            }
                            if(domain_state==3) $('#domain_state').find("#state").html('运行结束');

                            if(filtrate_state==2){
                                 $('#filtrate_state').show();
                                $('#filtrate_state').find("#state").html('正在运行');
                                $('#filtrate_state').find("#protected_filtrate").html(msg.data['filtrate_trusted_num']);
                                $('#filtrate_state').find("#counterfeit_filtrate").html(msg.data['filtrate_counterfeit_num']);
                                
                                $('#filtrate_state').find("#time").html(msg.data['filtrate_run_time']+'s');
                                
                            }
                            if(filtrate_state==3)  $('#filtrate_state').find("#state").html('运行结束');

                            if(web_save_state==2){
                                 $('#web_save_state').show();
                                $('#web_save_state').find("#state").html('正在运行');
                                $('#web_save_state').find("#request").html(msg.data['web_request_num']);
                                $('#web_save_state').find("#save").html(msg.data['web_save_num']);
                                
                                $('#web_save_state').find("#time").html(msg.data['web_save_run_time']+'s');
                                
                            }
                            if(web_save_state==3) $('#web_save_state').find("#state").html('运行结束');

                            if(feature_save_state==2){
                                $('#feature_save_state').show();
                                $('#feature_save_state').find("#state").html('正在运行');
                               
                                $('#feature_save_state').find("#save").html(msg.data['feature_save_num']);
                                
                                $('#feature_save_state').find("#time").html(msg.data['feature_save_run_time']+'s');
                                
                            }
                            if(feature_save_state==3) $('#feature_save_state').find("#state").html('运行结束');
                            if(search_state==2){
                               $('#search_state').show();
                                $('#search_state').find("#state").html('正在运行');
                                $('#search_state').find("#kword").html(msg.data['search_kword_num']);
                                $('#search_state').find("#url").html(msg.data['search_url_num']);
                                
                                $('#search_state').find("#time").html(msg.data['search_run_time']+'s'); 
                            }
                            if(search_state==3) $('#search_state').find("#state").html('运行结束');

                            if(pageblock_state==2){
                                $('#pageblock_state').show();
                                $('#pageblock_state').find("#state").html('正在运行');
                                $('#pageblock_state').find("#check").html(msg.data['title_check_num']);
                                $('#pageblock_state').find("#find").html(msg.data['title_find_num']);
                                
                                $('#pageblock_state').find("#time").html(msg.data['title_run_time']+
                                    's');
                                
                                
                            }
                            if(pageblock_state==3) $('#pageblock_state').find("#state").html('运行结束');
                            
                            if(title_state==2){
                               $('#title_state').show();
                                $('#title_state').find("#state").html('正在运行');
                                $('#title_state').find("#check").html(msg.data['title_check_num']);
                                $('#title_state').find("#find").html(msg.data['title_find_num']);
                                
                                $('#title_state').find("#time").html(msg.data['title_run_time']+
                                    's'); 
                            }
                            if(title_state==3)  $('#title_state').find("#state").html('运行结束');

                            if(view_collect_state==2){
                                $('#view_state').show();
                                $('#view_state').find("#state").html('正在运行');
                                $('#view_state').find("#check").html(msg.data['title_check_num']);
                                $('#view_state').find("#find").html(msg.data['title_find_num']);
                                
                                $('#view_state').find("#time").html(msg.data['title_run_time']+
                                    's');
                                
                                
                            }
                            if(view_collect_state==3)  $('#view_state').find("#state").html('运行结束');
                            


                            if(msg.data['task_state']==3)
                                clearInterval(flagLast);
                        };
                        if (msg.status == 0) 
                            alert('数据库连接失败！');        
                    } 
                });
            }
            
        });

        
        $(".view_stop").on("click", function(e) {
            $('#waiting').show();
            var taskid = $(this).attr("id"); 
           
            
            $.ajax({
                    type: "post",
                    url: "__APP__/Task/task_stop",
                    data:{
                        id:taskid
                    },
                    dataType: "json",
                    success: function(msg){
                        if (msg.status == 1 ) {
                            alert(msg.info);
                            location.reload();
                            
                        };
                        if (msg.status == 0) {
                            alert(msg.info); 
                            $('#waiting').hide();  
                           
                        };            
                    } 
            });
        });
        

        $(".view_result").on("click", function(e) {

            
            // var tasktime = '2015-04-25 16:40:40';
            // var ctask_id = 3;

            var tasktime = $(this).parent().prev().prev().prev().attr("id"); 
            var ctask_id = $(this).parent().prev().prev().prev().prev().attr("id"); 
                     


            $.ajax({
                    type: "post",
                    url: "__APP__/Task/checkProcess",
                    data:{
                        id   : ctask_id,
                        time : tasktime
                        },
                    dataType: "json",
                    success: function(msg){
                        $('#domain_state').hide();
                        $('#qt_state').hide();
                        $('#search_state').hide();
                        $('#filtrate_state').hide();
                        $('#web_save_state').hide();
                        $('#title_state').hide();
                        $('#pageblock_state').hide();
                        $('#whois_state').hide();
                        $('#feature_save_state').hide();
                        $('#view_state').hide();

                        if (msg.status == 1 ) {
                            var domain_state = msg.data['e_domain_state'];
                            var search_state = msg.data['e_search_state'];
                            var filtrate_state = msg.data['e_filtrate_state'];
                            var web_save_state = msg.data['e_web_save_state'];
                            var title_state = msg.data['e_title_state'];
                            var pageblock_state = msg.data['e_structure_state'];
                            var qt_state = msg.data['e_qt_crawler_state'];
                            var whois_search_state = msg.data['e_whois_search_state'];
                            var feature_save_state = msg.data['e_feature_save_state'];
                            var view_collect_state = msg.data['e_view_collect_state'];
                            
                            if(domain_state!=null){
                               $('#domain_state').show();
                                $('#domain_state').find("#state").html('运行结束');
                                $('#domain_state').find("#suspected").html(msg.data['domain_gray_url_num']);
                                $('#domain_state').find("#detected").html(msg.data['domain_detected_num']);
                                $('#domain_state').find("#changed").html(msg.data['domain_changed_all_num']);
                                $('#domain_state').find("#exist").html(msg.data['domain_changed_exist_num']);
                                
                                $('#domain_state').find("#time").html(msg.data['domain_run_time']+'s');
                                
                            }
                            if(filtrate_state!=null){
                                $('#filtrate_state').show();
                                $('#filtrate_state').find("#state").html('运行结束');
                                $('#filtrate_state').find("#protected_filtrate").html(msg.data['filtrate_trusted_num']);
                                $('#filtrate_state').find("#counterfeit_filtrate").html(msg.data['filtrate_counterfeit_num']);
                                
                                $('#filtrate_state').find("#time").html(msg.data['filtrate_run_time']+'s');
                                
                            }
                            if(qt_state!=null){
                                 $('#qt_state').show();
                                $('#qt_state').find("#state").html('运行结束');
                                
                                $('#qt_state').find("#qt_url").html(msg.data['qt_crawler_num']);
                                
                                $('#qt_state').find("#time").html(msg.data['qt_crawler_run_time']+'s');
                                
                            }
                            if(web_save_state!=null){
                                $('#web_save_state').show();
                                $('#web_save_state').find("#state").html('运行结束');
                                $('#web_save_state').find("#request").html(msg.data['web_request_num']);
                                $('#web_save_state').find("#save").html(msg.data['web_save_num']);
                                
                                $('#web_save_state').find("#time").html(msg.data['web_save_run_time']+'s');
                                
                            }
                            if(feature_save_state!=null){
                                $('#feature_save_state').show();
                                $('#feature_save_state').find("#state").html('运行结束');
                               
                                $('#feature_save_state').find("#save").html(msg.data['feature_save_num']);
                                
                                $('#feature_save_state').find("#time").html(msg.data['feature_save_run_time']+'s');
                                
                            }
                            if(search_state!=null){
                                $('#search_state').show();
                                $('#search_state').find("#state").html('运行结束');
                                $('#search_state').find("#kword").html(msg.data['search_kword_num']);
                                $('#search_state').find("#url").html(msg.data['search_url_num']);
                                
                                $('#search_state').find("#time").html(msg.data['search_run_time']+'s');
                                

                            }
                            if(pageblock_state!=null){
                               $('#pageblock_state').show();
                                $('#pageblock_state').find("#state").html('正在运行');
                                $('#pageblock_state').find("#check").html(msg.data['title_check_num']);
                                $('#pageblock_state').find("#find").html(msg.data['title_find_num']);
                                
                                $('#pageblock_state').find("#time").html(msg.data['title_run_time']+
                                    's');
                                
                            }
                            if(title_state!=null){
                                $('#title_state').show();
                                $('#title_state').find("#state").html('正在运行');
                                $('#title_state').find("#check").html(msg.data['title_check_num']);
                                $('#title_state').find("#find").html(msg.data['title_find_num']);
                                
                                $('#title_state').find("#time").html(msg.data['title_run_time']+
                                    's');
                                
                                
                            }
                             if(view_collect_state!=null){
                                $('#view_state').show();
                                $('#view_state').find("#state").html('运行结束');
                                $('#view_state').find("#check").html(msg.data['title_check_num']);
                                $('#view_state').find("#find").html(msg.data['title_find_num']);
                                
                                $('#view_state').find("#time").html(msg.data['title_run_time']+
                                    's');
                                
                                
                            }
                            if(qt_state!=null){
                                $('#qt_state').show();
                                $('#qt_state').find("#state").html('运行结束');
                                $('#qt_state').find("#qt_url").html(msg.data['qt_crawler_num']);
                               
                                $('#qt_state').find("#time").html(msg.data['qt_crawler_run_time']+
                                    's');
                            }


                        };
                        if (msg.status == 0) {
                            $('#domain').find("#state").html('已完成');
                            alert('数据库连接失败！');      
                        }; 
                          
                    } 
            });

        });
    });


</script>


</body>
</html>