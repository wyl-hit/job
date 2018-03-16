<?php if (!defined('THINK_PATH')) exit();?><!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
  <meta name="keywords" content="admin, dashboard, bootstrap, template, flat, modern, theme, responsive, fluid, retina, backend, html5, css, css3">
  <meta name="description" content="">
  <meta name="author" content="ThemeBucket">
  <link rel="shortcut icon" href="#" type="image/png">

  <title>钓鱼网站主动探测与验证系统后台管理</title>

  <!--icheck-->
  <link href="__TMPL__/js/iCheck/skins/minimal/minimal.css" rel="stylesheet">
  <link href="__TMPL__/js/iCheck/skins/square/square.css" rel="stylesheet">
  <link href="__TMPL__/js/iCheck/skins/square/red.css" rel="stylesheet">
  <link href="__TMPL__/js/iCheck/skins/square/blue.css" rel="stylesheet">

  <!--dashboard calendar-->
  <link href="__TMPL__/css/clndr.css" rel="stylesheet">


  <!--common-->
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
                    <img alt="" src="__TMPL__/images/photos/user-avatar.png" class="media-object">
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
                

             
                  <li class="menu-list"><a href=""><i class="fa fa-cogs"></i> <span>任务管理</span></a>
              
                    <ul class="sub-menu-list">
                        <li><a href="__APP__/Task/task_index.html"> 查看任务</a></li>
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
                                        <span class="thumb"><img src="__TMPL__/images/photos/user2.png" alt="" /></span>
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



        <!--body wrapper start-->
        

            <div class="row">
                <div class="col-md-12">
                    <section class="panel">
                        <header class="panel-heading">
                           
                        <span class="tools pull-right">
                            <a href="javascript:;" class="fa fa-chevron-down"></a>
                            
                         </span>
                        </header>
                        <div class="panel-body">
                           <div id="world_map" style="height: 700px;"></div>
                        </div>
                    </section>
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


                <script src="__TMPL__/js/echarts/dist/echarts.js"></script>
                <script type="text/javascript">
                    
                    // 路径配置
                    require.config({
                        paths: {
                            echarts: '__TMPL__/js/echarts'
                        }
                    });
        
                    // 使用
                    require(
                        [
                            'echarts',
                            'echarts/chart/map' // 使用柱状图就加载bar模块，按需加载
                        ],
                        function (ec) {
                            // 基于准备好的dom，初始化echarts图表
                            var myChart = ec.init(document.getElementById('world_map'));

                            var ecConfig = require('echarts/config');
                            var zrEvent = require('zrender/tool/event');
                            var curIndx = 0;
                          
                            
                            

                            //ajax获取地点信息
                            var placeList = new Array();

                            var request = false;
                            try {
                              request = new XMLHttpRequest();
                            } catch (failed) {
                              request = false;
                            }
                            if (!request)
                              alert("Error initializing XMLHttpRequest!");

                            var url = "__APP__/Index/getLocationInfo";

                            request.open("POST", url, true);
                            request.onreadystatechange = locationInfo;
                            request.send(null);

                            // clearInterval(timeTicket);
                            // var timeTicket = setInterval(locationInfo,2000);

                            function locationInfo() {
                                if (request.readyState == 4)
                                    if (request.status == 200){
                                        var response = request.responseText;
                                        response = JSON.parse(response);
                                        var data = response.data;
                                        var placeList = new Array();
                                       
                                        console.log(data);
                                        for (var i=0;i<data.length;i++) {
                                            
                                            placeList[i] = {};
                                            placeList[i]['name'] = data[i]['country'];
                                            placeList[i]['value'] = data[i]['count'];
                                          
                                        }
                                        console.log(placeList);
                                        

                                        var option = {
                                            title : {
                                                text: '仿冒网站分布图 ',
                                                
                                               
                                                x:'center',
                                                y:'top'
                                            },
                                            tooltip : {
                                                trigger: 'item',
                                                formatter : function (params) {
                                                    var value = (params.value + '').split('.');
                                                    value = value[0].replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,')
                                                            + '.' + value[1];
                                                    return params.seriesName + '<br/>' + params.name + ' : ' + params.value;
                                                }
                                            },
                                            toolbox: {
                                                show : true,
                                                orient : 'vertical',
                                                x: 'right',
                                                y: 'center',
                                                feature : {
                                                    mark : {show: true},
                                                    dataView : {show: true, readOnly: false},
                                                    restore : {show: true},
                                                    saveAsImage : {show: true}
                                                }
                                            },
                                            dataRange: {
                                                min: 0,
                                                max: 200,
                                                text:['High','Low'],
                                                realtime: false,
                                                calculable : true,
                                                color: ['orangered','yellow','lightskyblue']
                                            },
                                            series : [
                                                {
                                                    name: '仿冒网站数',
                                                    type: 'map',
                                                    mapType: 'world',
                                                    roam: true,
                                                    mapLocation: {
                                                        y : 60
                                                    },
                                                    itemStyle:{
                                                        emphasis:{label:{show:true}}
                                                    },

                                                    data : (function(){
                                                            var data = [];
                                                            var len = placeList.length;
                                                            while(len--) {
                                                                data.push({
                                                                    name : placeList[len].name,
                                                                    value : placeList[len].value
                                                                    
                                                                })
                                                            }
                                                            return data;
                                                        })(),

                                                   
                                                    nameMap : {
                                                                   'Afghanistan':'阿富汗',
                                                                   'Angola':'安哥拉',
                                                                   'Albania':'阿尔巴尼亚',
                                                                   'United Arab Emirates':'阿联酋',
                                                                   'Argentina':'阿根廷',
                                                                   'Armenia':'亚美尼亚',
                                                                   'French Southern and Antarctic Lands':'法属南半球和南极领地',
                                                                   'Australia':'澳大利亚',
                                                                   'Austria':'奥地利',
                                                                   'Azerbaijan':'阿塞拜疆',
                                                                   'Burundi':'布隆迪',
                                                                   'Belgium':'比利时',
                                                                   'Benin':'贝宁',
                                                                   'Burkina Faso':'布基纳法索',
                                                                   'Bangladesh':'孟加拉国',
                                                                   'Bulgaria':'保加利亚',
                                                                   'The Bahamas':'巴哈马',
                                                                   'Bosnia and Herzegovina':'波斯尼亚和黑塞哥维那',
                                                                   'Belarus':'白俄罗斯',
                                                                   'Belize':'伯利兹',
                                                                   'Bermuda':'百慕大',
                                                                   'Bolivia':'玻利维亚',
                                                                   'Brazil':'巴西',
                                                                   'Brunei':'文莱',
                                                                   'Bhutan':'不丹',
                                                                   'Botswana':'博茨瓦纳',
                                                                   'Central African Republic':'中非共和国',
                                                                   'Canada':'加拿大',
                                                                   'Switzerland':'瑞士',
                                                                   'Chile':'智利',
                                                                   'China':'中国',
                                                                   'Ivory Coast':'象牙海岸',
                                                                   'Cameroon':'喀麦隆',
                                                                   'Democratic Republic of the Congo':'刚果民主共和国',
                                                                   'Republic of the Congo':'刚果共和国',
                                                                   'Colombia':'哥伦比亚',
                                                                   'Costa Rica':'哥斯达黎加',
                                                                   'Cuba':'古巴',
                                                                   'Northern Cyprus':'北塞浦路斯',
                                                                   'Cyprus':'塞浦路斯',
                                                                   'Czech Republic':'捷克共和国',
                                                                   'Germany':'德国',
                                                                   'Djibouti':'吉布提',
                                                                   'Denmark':'丹麦',
                                                                   'Dominican Republic':'多明尼加共和国',
                                                                   'Algeria':'阿尔及利亚',
                                                                   'Ecuador':'厄瓜多尔',
                                                                   'Egypt':'埃及',
                                                                   'Eritrea':'厄立特里亚',
                                                                   'Spain':'西班牙',
                                                                   'Estonia':'爱沙尼亚',
                                                                   'Ethiopia':'埃塞俄比亚',
                                                                   'Finland':'芬兰',
                                                                   'Fiji':'斐',
                                                                   'Falkland Islands':'福克兰群岛',
                                                                   'France':'法国',
                                                                   'Gabon':'加蓬',
                                                                   'United Kingdom':'英国',
                                                                   'Georgia':'格鲁吉亚',
                                                                   'Ghana':'加纳',
                                                                   'Guinea':'几内亚',
                                                                   'Gambia':'冈比亚',
                                                                   'Guinea Bissau':'几内亚比绍',
                                                                   'Equatorial Guinea':'赤道几内亚',
                                                                   'Greece':'希腊',
                                                                   'Greenland':'格陵兰',
                                                                   'Guatemala':'危地马拉',
                                                                   'French Guiana':'法属圭亚那',
                                                                   'Guyana':'圭亚那',
                                                                   'Honduras':'洪都拉斯',
                                                                   'Croatia':'克罗地亚',
                                                                   'Haiti':'海地',
                                                                   'Hungary':'匈牙利',
                                                                   'Indonesia':'印尼',
                                                                   'India':'印度',
                                                                   'Ireland':'爱尔兰',
                                                                   'Iran':'伊朗',
                                                                   'Iraq':'伊拉克',
                                                                   'Iceland':'冰岛',
                                                                   'Israel':'以色列',
                                                                   'Italy':'意大利',
                                                                   'Jamaica':'牙买加',
                                                                   'Jordan':'约旦',
                                                                   'Japan':'日本',
                                                                   'Kazakhstan':'哈萨克斯坦',
                                                                   'Kenya':'肯尼亚',
                                                                   'Kyrgyzstan':'吉尔吉斯斯坦',
                                                                   'Cambodia':'柬埔寨',
                                                                   'South Korea':'韩国',
                                                                   'Kosovo':'科索沃',
                                                                   'Kuwait':'科威特',
                                                                   'Laos':'老挝',
                                                                   'Lebanon':'黎巴嫩',
                                                                   'Liberia':'利比里亚',
                                                                   'Libya':'利比亚',
                                                                   'Sri Lanka':'斯里兰卡',
                                                                   'Lesotho':'莱索托',
                                                                   'Lithuania':'立陶宛',
                                                                   'Luxembourg':'卢森堡',
                                                                   'Latvia':'拉脱维亚',
                                                                   'Morocco':'摩洛哥',
                                                                   'Moldova':'摩尔多瓦',
                                                                   'Madagascar':'马达加斯加',
                                                                   'Mexico':'墨西哥',
                                                                   'Macedonia':'马其顿',
                                                                   'Mali':'马里',
                                                                   'Myanmar':'缅甸',
                                                                   'Montenegro':'黑山',
                                                                   'Mongolia':'蒙古',
                                                                   'Mozambique':'莫桑比克',
                                                                   'Mauritania':'毛里塔尼亚',
                                                                   'Malawi':'马拉维',
                                                                   'Malaysia':'马来西亚',
                                                                   'Namibia':'纳米比亚',
                                                                   'New Caledonia':'新喀里多尼亚',
                                                                   'Niger':'尼日尔',
                                                                   'Nigeria':'尼日利亚',
                                                                   'Nicaragua':'尼加拉瓜',
                                                                   'Netherlands':'荷兰',
                                                                   'Norway':'挪威',
                                                                   'Nepal':'尼泊尔',
                                                                   'New Zealand':'新西兰',
                                                                   'Oman':'阿曼',
                                                                   'Pakistan':'巴基斯坦',
                                                                   'Panama':'巴拿马',
                                                                   'Peru':'秘鲁',
                                                                   'Philippines':'菲律宾',
                                                                   'Papua New Guinea':'巴布亚新几内亚',
                                                                   'Poland':'波兰',
                                                                   'Puerto Rico':'波多黎各',
                                                                   'North Korea':'北朝鲜',
                                                                   'Portugal':'葡萄牙',
                                                                   'Paraguay':'巴拉圭',
                                                                   'Qatar':'卡塔尔',
                                                                   'Romania':'罗马尼亚',
                                                                   'Russia':'俄罗斯',
                                                                   'Rwanda':'卢旺达',
                                                                   'Western Sahara':'西撒哈拉',
                                                                   'Saudi Arabia':'沙特阿拉伯',
                                                                   'Sudan':'苏丹',
                                                                   'South Sudan':'南苏丹',
                                                                   'Senegal':'塞内加尔',
                                                                   'Solomon Islands':'所罗门群岛',
                                                                   'Sierra Leone':'塞拉利昂',
                                                                   'El Salvador':'萨尔瓦多',
                                                                   'Somaliland':'索马里兰',
                                                                   'Somalia':'索马里',
                                                                   'Republic of Serbia':'塞尔维亚共和国',
                                                                   'Suriname':'苏里南',
                                                                   'Slovakia':'斯洛伐克',
                                                                   'Slovenia':'斯洛文尼亚',
                                                                   'Sweden':'瑞典',
                                                                   'Swaziland':'斯威士兰',
                                                                   'Syria':'叙利亚',
                                                                   'Chad':'乍得',
                                                                   'Togo':'多哥',
                                                                   'Thailand':'泰国',
                                                                   'Tajikistan':'塔吉克斯坦',
                                                                   'Turkmenistan':'土库曼斯坦',
                                                                   'East Timor':'东帝汶',
                                                                   'Trinidad and Tobago':'特里尼达和多巴哥',
                                                                   'Tunisia':'突尼斯',
                                                                   'Turkey':'土耳其',
                                                                   'United Republic of Tanzania':'坦桑尼亚联合共和国',
                                                                   'Uganda':'乌干达',
                                                                   'Ukraine':'乌克兰',
                                                                   'Uruguay':'乌拉圭',
                                                                   'United States of America':'美国',
                                                                   'Uzbekistan':'乌兹别克斯坦',
                                                                   'Venezuela':'委内瑞拉',
                                                                   'Vietnam':'越南',
                                                                   'Vanuatu':'瓦努阿图',
                                                                   'West Bank':'西岸',
                                                                   'Yemen':'也门',
                                                                   'South Africa':'南非',
                                                                   'Zambia':'赞比亚',
                                                                   'Zimbabwe':'津巴布韦'
                                                               }
                                                 }
                                            ]
                                        };

                                        // 为echarts对象加载数据 
                                        myChart.setOption(option); 
                                    }

                                    else if (request.status == 404)
                                        alert("Request URL does not exist");
                                else
                                    alert("Error: status code is " + request.status);
                            }

                            


                        }
                    );
                    
                </script>

<!-- Placed js at the end of the document so the pages load faster -->
<script src="__TMPL__/js/jquery-1.10.2.min.js"></script>
<script src="__TMPL__/js/jquery-ui-1.9.2.custom.min.js"></script>
<script src="__TMPL__/js/jquery-migrate-1.2.1.min.js"></script>
<script src="__TMPL__/js/bootstrap.min.js"></script>
<script src="__TMPL__/js/modernizr.min.js"></script>
<script src="__TMPL__/js/jquery.nicescroll.js"></script>

<!--easy pie chart-->
<script src="__TMPL__/js/easypiechart/jquery.easypiechart.js"></script>
<script src="__TMPL__/js/easypiechart/easypiechart-init.js"></script>

<!--Sparkline Chart-->
<script src="__TMPL__/js/sparkline/jquery.sparkline.js"></script>
<script src="__TMPL__/js/sparkline/sparkline-init.js"></script>

<!--icheck -->
<script src="__TMPL__/js/iCheck/jquery.icheck.js"></script>
<script src="__TMPL__/js/icheck-init.js"></script>

<!-- jQuery Flot Chart-->
<script src="__TMPL__/js/flot-chart/jquery.flot.js"></script>
<script src="__TMPL__/js/flot-chart/jquery.flot.tooltip.js"></script>
<script src="__TMPL__/js/flot-chart/jquery.flot.resize.js"></script>
<script src="__TMPL__/js/flot-chart/jquery.flot.pie.resize.js"></script>
<script src="__TMPL__/js/flot-chart/jquery.flot.selection.js"></script>
<script src="__TMPL__/js/flot-chart/jquery.flot.stack.js"></script>
<script src="__TMPL__/js/flot-chart/jquery.flot.time.js"></script>
<script src="__TMPL__/js/main-chart.js"></script>

<!--common scripts for all pages-->
<script src="__TMPL__/js/scripts.js"></script>


</body>
</html>