<?php if (!defined('THINK_PATH')) exit();?><!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
  <meta name="description" content="">
  <meta name="author" content="ThemeBucket">
  <link rel="shortcut icon" href="#" type="image/png">

  <title>查看被保护网站详情</title>

  <!--data table-->
  <link rel="stylesheet" href="__TMPL__/js/data-tables/DT_bootstrap.css" />

  <link href="__TMPL__/css/style.css" rel="stylesheet">
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

                <li class="menu-list "><a href=""><i class="fa fa-book"></i> <span>白名单管理</span></a>
                    <ul class="sub-menu-list">
                       <li><a href="__APP__/Wlist/wlist_index.html"> 查看被保护网站名单</a></li>
                        <li><a href="__APP__/Wlist/wlist_trusted.html"> 查看被信任网站名单</a></li>
                        <li><a href="__APP__/Wlist/wlist_add.html"> 添加白名单</a></li>
                       

                    </ul>
                </li>
                  <li class="menu-list nav-active"><a href=""><i class="fa fa-laptop"></i> <span>可疑名单管理</span></a>
                    <ul class="sub-menu-list">
                        <li class="active"><a href="__APP__/Slist/slist_index.html"> 查看可疑名单</a></li>
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
                

             
                  <li class="menu-list"><a href=""><i class="fa fa-cogs"></i> <span>任务管理</span></a>
              
                    <ul class="sub-menu-list">
                        <li ><a href="__APP__/Task/task_index.html"> 查看任务</a></li>
                        <li><a href="__APP__/Task/task_add.html"> 添加任务</a></li>
                        
                        <li><a href="__APP__/Task/task_result.html"> 查看任务状态</a></li>
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
                <li>
                    <a href="__APP__/Index/indexMain.html">首页</a>
                </li>
                <li>
                    <a href="#">可疑网站管理</a>
                </li>
                <li>
                    <a href="__APP__/Slist/slist_index.html">查看可疑网站</a>
                </li>
                <li class="active"> 可疑网站详情 </li>
            </ul>
        </div>
        <!-- page heading end-->

        <!--body wrapper start-->
        <div class="wrapper">

              <div class="row" >
            <div class="col-lg-12" >
                <section class="panel" id ="confirm">
                    <header class="panel-heading">
                       确认可疑网站为仿冒网站
                    </header>
                    <div class="panel-body" >
                       
                                    
                                   
                                 <form class="cmxform form-horizontal adminex-form" method="post" id = "confirmForm" action=<?php echo U('Slist/confirmGraylist');?>>  

                                     <div class="form-group ">
                                        <label for="ccomment" class="control-label col-lg-2">待确认可疑网站id </label>
                                         <div class="col-lg-4">
                                         <input class=" form-control" id="urlid" name = "urlid" size="16" minlength="2" type="text"  required/>
                                     </div>
                                             
                                    </div>
                                    <div class="form-group"   >
                                        <label class="col-sm-2 control-label col-lg-2" for="inputSuccess">选择仿冒网站类型</label>
                                         <div class="col-lg-4">
                                           <select id="country" name ="country" class="form-control m-bot15 s_country">
                                                <option value="" >选择国家</option>
                                                <option value="中国" >国内</option>
                                                 <option value="*" >国外</option>
                                                               
                                            </select>

                                          
                                           </div>
                                        <div class="col-lg-4">
                                          <select id="type" name ="type" class="form-control m-bot15 s_type">
                                                <option value="">选择类别</option>
                                                     <?php if(is_array($type)): $i = 0; $__LIST__ = $type;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><option value="<?php echo ($one); ?>"><?php echo ($one); ?></option><?php endforeach; endif; else: echo "" ;endif; ?>
                                                               
                                                </select>

                                          
                                           </div>
                                            
                                    </div>
                                    <div class="form-group"   >
                                        <label class="col-sm-2 control-label col-lg-2" for="inputSuccess">选择被仿冒网站</label>
                                        <div class="col-lg-4">
                                          <select id="source_website" name ="source_website" class="form-control m-bot15">
                                                <option value="">选择被仿冒网站</option>
                                                  <?php if(is_array($source)): $i = 0; $__LIST__ = $source;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><option value=""></option><?php endforeach; endif; else: echo "" ;endif; ?>
                                                             
                                            </select>
                                        </div>
                                    </div>
                                         <div class="form-group"   >
                                            <label class="col-sm-2 control-label col-lg-2" for="inputSuccess">新增被仿冒网站</label>
                                            <div class="col-lg-4">
                                            <input class=" form-control" id="new_website"  size="16" name="new_website" minlength="2" type="text" placeholder="在此填写新增被仿冒网站域名" /> </div>

                                            <div class="col-lg-4">
                                            <input class=" form-control" id="new_wname"  size="16" name="new_wname" minlength="2" type="text" placeholder="在此填写新增被仿冒网站名称" />
                                             
                                           </div>
                                            
                                    </div>
                                    <div class="form-group ">
                                        <label for="ccomment" class="control-label col-lg-2">备注 </label>
                                        <div class="col-lg-10">
                                            <textarea class="form-control " id="ccomment" name="comment" ></textarea>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <div class="col-lg-offset-2 col-lg-10" align ="right">
                                            <button class="btn btn-primary " >提交</button>
                                            <button class="btn btn-default" >重置</button>
                                        </div>
                                    </div>
                                </form>
                                

                    </div>
                </section>
            </div>
           
        </div>
    <div class= "row" id= "text_web_save">
      <div class="col-sm-12">
         <section class="panel">
           <header class="panel-heading">
            可疑网站信息详情
            <span class="tools pull-right">
                <a href="javascript:;" class="fa fa-chevron-down"></a>
               
             </span>

           </header>
          <div class="panel-body">
           
            
            <table class="table  table-hover general-table">
                  <thead>
                    <tr>
                        <th> id</th>
                        <th> url</th>
                        <th >添加时间</th>
                        <th> 网站title</th>
                        <th >网页关键字</th>
                        <th >操作</th>
                        
                        

                    </tr>
                    </thead>
                    <tbody>
                        <?php if(is_array($gray_feature)): $i = 0; $__LIST__ = $gray_feature;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                <td width="5%" id="<?php echo ($one["id"]); ?>"><?php echo ($one["id"]); ?></td>
                                <td width="15%"><?php echo ($one["url"]); ?></td>
                                <td width="10%"><?php echo ($one["add_time"]); ?></td>
                                <td width="10%"><?php echo ($one["title"]); ?></td>
                                <td width="65%"><?php echo ($one["kword"]); ?></td>
                                <td width="5%">
                                    <a href="#" class="btn view">确认</a>
                                    <a href="#" class="btn view_delete" id="<?php echo ($one["id"]); ?>">删除</a>
                                    <a href="#" class="btn view_addM" id="<?php echo ($one["id"]); ?>">添加为重点监测</a>
                               </td>
                              
                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                      
                        
                           
                      

                    </tbody>
            </table>


        
        </div>
      </section>
     </div>
    </div>
    <div class= "row" id= "text_web_save">
      <div class="col-sm-4">
        <section class="panel">
           <header class="panel-heading">
            网页关键字比对引擎结果
            <span class="tools pull-right">
                <a href="javascript:;" class="fa fa-chevron-down"></a>
               
             </span>

           </header>
            <div class="panel-body">
           
            
                <table class="table  table-hover general-table">
                    <tbody>
                        <?php if(is_array($gray_result)): $i = 0; $__LIST__ = $gray_result;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                <th  width="45%">被仿冒网站</th>
                                <td><?php echo ($one["title_source_result"]); ?></td>
                                
                               
                            </tr>
                            <tr>
                                <th width="45%">相似仿冒网站</th>
                                <td ><?php echo ($one["title_counterfeit_result"]); ?></td>
                               
                            </tr>
                            <tr>
                                <th  width="45%"> 模板号</th>
                                <td><?php echo ($one["title_template_num"]); ?></td>
                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                      
                        
                    </tbody>
                    

                </table>
        
            </div>
        </section>
      </div>

   
      <div class="col-sm-4">
        <section class="panel">
           <header class="panel-heading">
            网页结构比对引擎结果
            <span class="tools pull-right">
                <a href="javascript:;" class="fa fa-chevron-down"></a>
               
             </span>

           </header>
            <div class="panel-body">
           
            
                <table class="table  table-hover general-table">
                    <tbody>
                        <?php if(is_array($gray_result)): $i = 0; $__LIST__ = $gray_result;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                <th  width="45%">被仿冒网站</th>
                                <td><?php echo ($one["structure_source_result"]); ?></td>
                                
                               
                            </tr>
                            <tr>
                                <th width="45%">相似仿冒网站</th>
                                <td ><?php echo ($one["structure_counterfeit_result"]); ?></td>
                               
                            </tr>
                            <tr>
                                <th  width="45%"> 模板号</th>
                                <td><?php echo ($one["structure_template_num"]); ?></td>
                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                      
                        
                    </tbody>
                    

                </table>
        
            </div>
        </section>
      </div>

   
      <div class="col-sm-4">
        <section class="panel">
           <header class="panel-heading">
            网页视觉比对引擎结果
            <span class="tools pull-right">
                <a href="javascript:;" class="fa fa-chevron-down"></a>
               
             </span>

           </header>
            <div class="panel-body">
           
            
                <table class="table  table-hover general-table">
                    <tbody>
                        <?php if(is_array($gray_result)): $i = 0; $__LIST__ = $gray_result;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                <th  width="45%">被仿冒网站</th>
                                <td><?php echo ($one["view_source_result"]); ?></td>
                                
                               
                            </tr>
                            <tr>
                                <th width="45%">相似仿冒网站</th>
                                <td ><?php echo ($one["view_counterfeit_result"]); ?></td>
                               
                            </tr>
                            <tr>
                                <th  width="45%"> 模板号</th>
                                <td><?php echo ($one["view_template_num"]); ?></td>
                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                      
                        
                    </tbody>
                    

                </table>
        
            </div>
        </section>
      </div>

    </div>
    <div class= "row">
        <div class="col-sm-12">
         <section class="panel">
           <header class="panel-heading">
           网站截图
            <span class="tools pull-right">
                <a href="javascript:;" class="fa fa-chevron-down"></a>
               
             </span>

           </header>
          <div class="panel-body">
         <div id="gallery" class="media-gal">
             <?php if(is_array($gray_feature)): $i = 0; $__LIST__ = $gray_feature;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><div class="col-sm-6">
                                    <header class="panel-heading">
                                     网页截图
                                     

                                    </header>
                                    <a href="<?php echo ($one["webpage"]); ?>" >
                                        <img src="<?php echo ($one["webpage"]); ?>" width= "80%" alt="" />
                                    </a>
                                   
                                </div>

                                <div  class="col-sm-6" >
                                     <header class="panel-heading">
                                     结构截图
                                     

                                    </header>

                                    <a href="<?php echo ($one["blockpage"]); ?>">
                                        <img src="<?php echo ($one["blockpage"]); ?>"  width= "80%" alt="" />
                                    </a>
                                    
                                </div><?php endforeach; endif; else: echo "" ;endif; ?>
                               
        </div>
         </div>
      </section>
     </div>
    </div>

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

<!--script for editable table-->
<script src="__TMPL__/js/editable-table.js"></script>

<!-- END JAVASCRIPTS -->
<script>
    jQuery(document).ready(function() {
        EditableTable.init();
    });

    $(document).ready(function(){
       
        $('#confirm').hide();

        $(".view").on("click", function(e) { 
            

            $('#confirm').show();

           
        });
        $(".view_delete").on("click", function(e) { 
            var id = $(this).attr('id');
            $.ajax({
                    type: "post",
                    url: "__APP__/Slist/delete_slist",
                    data:{
                        id   : id
                       
                        },
                    dataType: "json",
                    success: function(msg){
                         alert(msg.info);
 

                       
                          
                    } 
            });
 
        });
        $(".view_addM").on("click", function(e) { 
            var id = $(this).attr('id');
            alert(id);
            $.ajax({
                    type: "post",
                    url: "__APP__/Slist/add_monitor",
                    data:{
                        id   : id
                        },
                    dataType: "json",
                    success: function(msg){
                         alert(msg.info);
 

                       
                          
                    } 
            });
 
        });
        $(".s_country").on("change", function(e) {

            
            var s_type = document.getElementById('type');
            var location = $(this).val();
            alert(location);
            
            $.ajax({
                    type: "post",
                    url: "__APP__/Slist/checkType",
                    data:{
                        country   : location
                       
                        },
                    dataType: "json",
                    success: function(msg){
 

                        if (msg.status != 1 ) {
                           
                            s_type.options.length=1;
                            for(i=0;i<msg.status;i++){
                                var op = new Option(msg.data[i],msg.data[i]);
                               
                                s_type.add(op);
                            }
                           
                        };
                        if (msg.status == 0) {
                           
                            alert(msg.info);      
                        }; 
                          
                    } 
            });

        });
        $(".s_type").on("change", function(e) {

            
            var source_website = document.getElementById('source_website');
            var type = $(this).val();
           
            
            
            $.ajax({
                    type: "post",
                    url: "__APP__/Slist/checkWebsite",
                    data:{
                        
                        type  :  type
                       
                        },
                    dataType: "json",
                    success: function(msg){
 

                        if (msg.status != 0 ) {
                            alert(msg.status);
                            
                            source_website.options.length=1;
                            for(i=0;i<msg.status;i++){

                                var op = new Option(msg.data[i]['source_name'],msg.data[i]['id']);
                                source_website.add(op);
                            }
                           
                        };
                        if (msg.status == 0) {
                           
                            alert(msg.info);      
                        }; 
                          
                    } 
            });

        });

    });




</script>



</body>
</html>