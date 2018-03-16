<?php if (!defined('THINK_PATH')) exit();?><!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
  <meta name="description" content="">
  <meta name="author" content="ThemeBucket">
  <link rel="shortcut icon" href="#" type="image/png">

  <title>可疑名单管理</title>
  <script>  

  function del(id)
    {  
        if(confirm("确定要删除吗？"))
        {
            var url = "index.html";
            
            window.location.href="<?php echo U('Wlist/protected_delete');?>";    
        }
    
    }
        function test(o) {  
            if (!o.checked) {  
                return;  
            }  
            var tr = o.parentNode.parentNode; 
            var items = $('[name = "item"]:checkbox:checked'); 
            var tds = tr.cells;  
            var value = o.value;
            var str = "you click ";  
            for(var i = 0;i < items.length;i++){  
                if (i < 3) {  
                    str = str + tds[i].innerHTML + "--";  
                    stt =value;
                }  
            }  
           window.location.href="<?php echo U('Wlist/trusted_delete');?>";
        } 
       
    </script>  

  <!--dynamic table-->
  <link href="__TMPL__/js/advanced-datatable/css/demo_page.css" rel="stylesheet" />
  <link href="__TMPL__/js/advanced-datatable/css/demo_table.css" rel="stylesheet" />
  <link rel="stylesheet" href="__TMPL__/js/data-tables/DT_bootstrap.css" />

  <link href="__TMPL__/css/style.css" rel="stylesheet">
  <link rel="stylesheet" href="__TMPL__/css/style_time.css" media="screen" type="text/css" />
  <link href="__TMPL__/css/style-responsive.css" rel="stylesheet">

 <!--pickers css-->
 



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

                <li class="menu-list"><a href=""><i class="fa fa-book nav-active"></i> <span>白名单管理</span></a>
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
                 <li class=""> 可疑名单管理 </li>
                <li class="active"> 查看可疑 </li>
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
                                    <a href="#home" data-toggle="tab">探测可疑灰名单</a>
                                </li>
                                <li class="">
                                    <a href="#about" data-toggle="tab">待验证可疑灰名单</a>
                                </li>
                               
                            </ul>
                        </header>
                        <div class="panel-body">
                            <div class="tab-content">
                                <div class="tab-pane active" id="home">
                                    
                                            
                                     <form class="cmxform form-horizontal adminex-form" id="commentForm" method="post" action=<?php echo U('Slist/slist_delete');?> >
                                    
                                     <div class="adv-table">
                                    <div class="clearfix">
                                            <div class="btn-group pull-right">
                                             <button class="btn btn-primary"  >批量删除</button>
                                            </div>
                                            
                                        </div>
                                    <table  class="display table table-bordered table-striped" id="dynamic-table">
                                        <thead>
                                        <tr>
                                            <th>可疑灰名单名称</th>
                                            <th>灰名单生成引擎类型</th>
                                            <th>生成时间</th>
                                            <th>用户id</th>
                                            <th>任务id</th>
                                            <th>数量</th>
                                            <th>选择</th>
                                            <th>操作</th>
                                           
                                        </tr>
                                        </thead>
                                        
                                        <tbody>
                                           
                                          <?php if(is_array($suspected_list)): $i = 0; $__LIST__ = $suspected_list;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                                <td><?php echo ($one["slist_name"]); ?></td>
                                                <td><?php if(($one["type"] == 1)): ?>用户输入
                                                    
                                                    <?php else: ?>探测<?php endif; ?>
                                                </td>
                                                <td><?php echo ($one["slist_gtime"]); ?></td>
                                                <td><?php echo ($one["user_id"]); ?> </td>
                                                <td id = "<?php echo ($one["task_id"]); ?>"><?php echo ($one["task_id"]); ?></td>
                                                <td><?php echo ($one["slist_num"]); ?></td>
                                                <td><input type="checkbox"  name = "ids[]" value = "<?php echo ($one["object_id"]); ?>" /></td>
                                                <td>
                                                    <a href="javascript:window.location.href='suspect_check/id/<?php echo ($one["object_id"]); ?>/type/<?php echo ($one["type"]); ?>'; " class="btn">下载</a>
                                                    <a href="#" class="btn view3" id="<?php echo ($one["object_id"]); ?>">检测</a>
                                                   
                                                </td>

                                             
                                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                                        </tbody>
                                        
                                    </table>
                                  
                                    </div>
                                </form>
                                    
                              
                            </div>
                                <div class="tab-pane" id="about">
                                    <div class="adv-table editable-table ">
              
                                    <div class="space15"></div>
                                    <form class="cmxform form-horizontal adminex-form" id="commentForm" method="post" action=<?php echo U('Slist/gray_delete');?> >
                                    
                                     <div class="adv-table">
                                    <div class="clearfix">
                                            <div class="btn-group pull-right">
                                             <button class="btn btn-primary"  >批量删除</button>
                                            </div>
                                            
                                        </div>
                                    <table class="table table-striped table-hover table-bordered" id="editable-sample">
                                        <thead>
                                            <tr>
                                                <th>可疑URL</th>
                                                <th>添加时间</th>
                                                <th>发现来源</th>
                                                <th><input type="checkbox" class="checkboxCtrl" group ="ids"/></th>
                                                <th>查看详情</th>
                                                               
                                                               
                                            </tr>
                                        </thead>              
                                        <tbody>                     
                                            <?php if(is_array($gray_list)): $i = 0; $__LIST__ = $gray_list;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                                    <td><?php echo ($one["url"]); ?></td>
                                                                   
                                                    <td><?php echo ($one["add_time"]); ?></td>
                                                    <td><?php echo ($one["source"]); ?></td>

                                                    <td><input type="checkbox"  name = "ids[]" value = "<?php echo ($one["id"]); ?>" /></td>
                                                    <td>
                                                        <a href="javascript:window.location.href='checkDetail/id/<?php echo ($one["id"]); ?>';">查看详情</a>
                                                        <a href="javascript:window.location.href='updateInfo/id/<?php echo ($one["id"]); ?>';" >更新信息</a>
                                                    </td>

                                                                 
                                                </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                                        </tbody>
                                    </table>
                                </div>
                            </form>
                                    </div>  
                                    
                                </div>
                                
                            </div>
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

<!--dynamic table-->
<script type="text/javascript" language="javascript" src="__TMPL__/js/advanced-datatable/js/jquery.dataTables.js"></script>
<script type="text/javascript" src="__TMPL__/js/data-tables/jquery.dataTables.js"></script>
<script type="text/javascript" src="__TMPL__/js/data-tables/DT_bootstrap.js"></script>
<!--dynamic table initialization -->
<script src="__TMPL__/js/dynamic_table_init.js"></script>
<!--script for editable table-->
<script src="__TMPL__/js/editable-table.js"></script>
<!--common scripts for all pages-->
<script src="__TMPL__/js/scripts.js"></script>





<!-- END JAVASCRIPTS -->
<script type="text/javascript">
    jQuery(document).ready(function() {
        EditableTable.init();
    });
   


    $(document).ready(function(){
        var i =0;
        var word='';
        var url='';
        $('#protected').hide();
        $('#kword').hide();
        $('#waiting').hide();
        $(".view").on("click", function(e) {
            var taskid = $(this).parent().prev().prev().attr("id"); 
            $.ajax({
                    type: "post",
                    url: "__APP__/Slist/checkProtected",
                    data:{
                        id:taskid
                    },
                    dataType: "json",
                    success: function(msg){
                        if (msg.status == 1 ) { 
                            for(i=0;msg.data[i]!='';i++){
                                url = url+'<li>'+msg.data[i]+'</li>';
                            }
                            $('#protected').find('#protected_list').html(url);
                            $('#config').show();
                            $('#protected').show();
                            url='';
                        };
                        if (msg.status == 0) {
                            alert('数据库连接失败！');      
                        };            
                    } 
            });
        });
        $(".view1").on("click", function(e) {
            var taskid = $(this).parent().prev().prev().attr("id"); 
            
            $.ajax({
                    type: "post",
                    url: "__APP__/Slist/checkKword",
                    data:{
                        id:taskid
                    },
                    dataType: "json",
                    success: function(msg){
                        if (msg.status == 1 ) {
                            
                            for(i=0;msg.data[i]!='';i++){
                                word = word+'<li>'+msg.data[i]+'</li>';
                            }
                            if(i!=0)
                                $('#kword').find('#kword_list').html(word);  
                            else
                                $('#kword').find('#kword_list').html('本可疑名单未对应敏感关键字。');           
                            $('#kword').show();
                            word='';
                        };
                        if (msg.status == 0) {
                            alert('数据库连接失败！');      
                        };            
                    } 
            });
        });
         $(".view_update").on("click", function(e) {
            var id = $(this).attr('id');
            
            $.ajax({
                    type: "post",
                    url: "__APP__/Wlist/updateInfo",
                    data:{
                        id:id
                    },
                    dataType: "json",
                    success: function(msg){
                        alert(msg.info);      
                                
                    } 
            });
        });

        $(".view3").on("click", function(e) {
            $('#waiting').show();
            var objecid = $(this).attr("id"); 
            
            $.ajax({
                    type: "post",
                    url: "__APP__/Slist/suspect_runtask",
                    data:{
                        id:objecid
                    }, 
                    dataType: "json",
                    success: function(msg){
                        if (msg.status == 1 ) {
                            alert(msg.info);
                            $('#waiting').hide();
                            
                        };
                        if (msg.status == 0) {
                            alert(msg.info);   
                            $('#waiting').hide();   
                        };            
                    } 
            });
        });
    });



</script>

</body>
</html>