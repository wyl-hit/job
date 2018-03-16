<?php if (!defined('THINK_PATH')) exit();?><!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
  <meta name="description" content="">
  <meta name="author" content="ThemeBucket">
  <link rel="shortcut icon" href="#" type="image/png">

  <title>添加任务</title>

  <link href="__TMPL__/css/style.css" rel="stylesheet">
  <link href="__TMPL__/css/style-responsive.css" rel="stylesheet">
  <link href="__TMPL__/css/smart_wizard.css" rel="stylesheet" type="text/css">
  <link href="__TMPL__/css/demo_style.css" rel="stylesheet" type="text/css">
 <!--dynamic table-->
  <link href="__TMPL__/js/advanced-datatable/css/demo_page.css" rel="stylesheet" />
  <link href="__TMPL__/js/advanced-datatable/css/demo_table.css" rel="stylesheet" />
  <link rel="stylesheet" href="__TMPL__/js/data-tables/DT_bootstrap.css" />

  <link href="__TMPL__/css/style.css" rel="stylesheet">
  <link href="__TMPL__/css/style-responsive.css" rel="stylesheet">

  <script type="text/javascript" src="__TMPL__/js/jquery-1.4.2.min.js"></script>
  <script type="text/javascript" src="__TMPL__/js/jquery.smartWizard-2.0.min.js"></script>
  <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
  <!--[if lt IE 9]>
  <script src="js/html5shiv.js"></script>
  <script src="js/respond.min.js"></script>
  <![endif]-->
  <script type="text/javascript">

   
   
   
//1 在第一个选项中，使用一个下拉列表来选择值    （测试时用 radio 获取值时出现问题）
//2 在换页时，判断下拉列表的值
//3 使用 hide()   和 show() 函数来显示，第二个选项中相应的值


    $(document).ready(function(){

      $('#counterfeit_list').hide();
        // Smart Wizard         
      $('#wizard').smartWizard({transitionEffect:'slideleft',onLeaveStep:leaveAStepCallback,enableFinishButton:true});
      
      
      //换页函数 
      function leaveAStepCallback(obj){
        var step_num= obj.attr('rel');  //获取换页number
        return validateSteps(step_num);//验证当前步骤即当前页
      }
      
      //提交按钮，验证所有页
      function onFinishCallback(){
       if(validateAllSteps()){
        $('taskForm').submit();
       }
      }
        });
      //验证所有步骤是否正确，如果错误，则打印？页有错
       function validateAllSteps(){
       var isStepValid = true;
       //第一步
       if(validateStep1() == false){
         isStepValid = false;
         $('#wizard').smartWizard('setError',{stepnum:1,iserror:true});         
       }else{
         $('#wizard').smartWizard('setError',{stepnum:1,iserror:false});
       }
       //第二步
       if(validateStep2() == false){
         isStepValid = false;
         $('#wizard').smartWizard('setError',{stepnum:2,iserror:true});         
       }else{
         $('#wizard').smartWizard('setError',{stepnum:2,iserror:false});
       }
       //第三步
       if(validateStep3() == false){
         isStepValid = false;
         $('#wizard').smartWizard('setError',{stepnum:3,iserror:true});         
       }else{
         $('#wizard').smartWizard('setError',{stepnum:3,iserror:false});
       }
       
       if(!isStepValid){
          $('#wizard').smartWizard('showMessage','Please correct the errors in the steps and continue');
       }
              
       return isStepValid;
    }   

    jQuery(document).ready(function() {
        EditableTable.init();
    });

    //检测函数
    
      function validateSteps(step){
       var isStepValid = true;
      // validate step 1
      if(step == 1){
      
      <!--通过第一页的数据选择控制第二页的显示-->
       var task_type = document.getElementsByName("tasktype");

       var enegine_type = $('#engine').val();
       var chk_counterfeit = document.getElementById('counterfeit_choose');
       var chk_protected = document.getElementById('protected_choose');
       
       if(task_type[1].checked)//选择验证任务 --需要选择灰名单
       {
          $('#keywords').hide();    
          $('#changerules').hide(); 
          $('#suspectedlist').show(); 
          

          $('#counterfeit_list').hide(); 
          $('#protected_list').hide(); 
         
          
          chk_protected.disabled = true;
          chk_counterfeit.disabled = true;              
          $('#step-3').find("#detectedMessage").html('您当前选择的任务类型无需选择待检测名单'); 
       }

       else if(task_type[0].checked)//选择探测任务
       {

        //选择域名变换规则---需要选择规则 白名单 黑名单
         if(enegine_type == '01')
          {
            $('#changerules').show();    
            $('#keywords').hide(); 
            $('#suspectedlist').hide(); 
            $('#step-3').find("#detectedMessage").html('您当前选择的任务类型至少选一种检测类型');
          }
             
          //选额探测任务-元搜索/微波   ————需要关键字 
          else{

             $('#keywords').show();    
             $('#changerules').hide(); 
             $('#suspectedlist').hide(); 
             $('#protected_list').hide();  
             $('#step-3').find('#detectedMessage').html('您当前选择的任务类型不需要选择检测名单，请点击完成。');
          }
       }
       //选择探测及验证任务
       else
       {

         //选择域名变换规则---需要选择规则 白名单 黑名单
            if(enegine_type == '01')
            {
               $('#changerules').show();    
               $('#keywords').hide(); 
               $('#suspectedlist').hide(); 

               $('#step-3').find("#detectedMessage").html('您当前选择的任务类型被保护网站为必选，仿冒网站为可选');
            }
            //选择关键字 ---选择关键字 
            else
            {
               $('#keywords').show();    
               $('#changerules').hide(); 
               $('#suspectedlist').hide();
               $('#counterfeit_list').hide(); 
               $('#protected_list').hide(); 
               chk_protected.disabled = true;
               chk_counterfeit.disabled = true;   

                
               $('#step-3').find("#detectedMessage").html('您当前选择的任务类型无需选择待检测名单');  
            }

       }
       
       
    <!--控制结束-->
    //验证第一页
       if(validateStep1() == false){

          isStepValid = false; 
          $('#wizard').smartWizard('showMessage','Please correct the errors in step'+step+ ' and click next.');
          $('#wizard').smartWizard('setError',{stepnum:step,iserror:true});         
        }

        else
            $('#wizard').smartWizard('setError',{stepnum:step,iserror:false});
        
       
    } 
      //验证第二步
        if(step == 2){
        if(validateStep2() == false ){
          isStepValid = false; 
          $('#wizard').smartWizard('showMessage','Please correct the errors in step'+step+ ' and click next.');
          $('#wizard').smartWizard('setError',{stepnum:step,iserror:true});         
        }else{
          $('#wizard').smartWizard('setError',{stepnum:step,iserror:false});
        }
      } 
        //验证第三步
       if(step == 3){
        if(validateStep3() == false ){
          isStepValid = false; 
          $('#wizard').smartWizard('showMessage','Please correct the errors in step'+step+ ' and click next.');
          $('#wizard').smartWizard('setError',{stepnum:step,iserror:true});         
        }else{
          $('#wizard').smartWizard('setError',{stepnum:step,iserror:false});
        }
      } 
       
       return isStepValid;
      }


        //步骤一验证
        function validateStep1(){
       var isValid = true; 
       // 任务名称必填
       var un = $('#taskname').val();

       if(!un && un.length <= 0){
         isValid = false;
         $('#msg_taskname').html('请填写任务名称').show();
       }else{
         $('#msg_taskname').html('').hide();
       }
      

       //验证任务引擎，必须选择一项探测方法
       var taskengine = $('#engine').val();
       var task_type = document.getElementsByName("tasktype");
       
       if(task_type[1].checked||taskengine!='0')
        $('#msg_taskengine').html('').hide();
       else{
         isValid = false;
         $('#msg_taskengine').html('请选择探测引擎类型').show();
       }


      
        //验证任务类型，如果当前验证引擎checkbox可选，则选择的是探测及验证任务，故验证引擎至少选一个

       var chks = document.getElementsByName("engine1[]");
       if(chks[0].disabled==false)
         {
          //调用checkbox检测函数，检测验证引擎的选择情况
            if(validateChecked('engine1[]')){
                 $('#msg_taskengine1').html('').hide();
                }
                
            
            else{
                isValid = false;
                $('#msg_taskengine1').html('请至少选择一种验证方式').show();
              }        
         }

       return isValid;
      }  
      //验证第二步
        function validateStep2(){
       
       
            var isValid = false;

            //配置文件至少选一项
            if(validateChecked('pathrules[]')||validateChecked('urlrules[]')||validateChecked('toprules[]')||validateChecked('kwords[]')||validateChecked('slists')||validateChecked('grayids[]')){
                 $('#msg_toprules').html('').hide();
                 $('#msg_kwords').html('').hide();
                 $('#msg_slists').html('').hide();

                 isValid = true;
            }
            else{
                $('#msg_toprules').html('请至少选择一项变换规则').show();
                $('#msg_kwords').html('请至少选择一项敏感关键字').show();
                $('#msg_slists').html('请选择一条灰名单列表').hide();
            }
       
        return isValid;
      } 
      //验证第三步
      function validateStep3(){
          var task_type = document.getElementsByName("tasktype");
          var enegine_type = $('#engine').val();
          var isValid = false;

          if(task_type[1].checked)//验证任务
          {
           
              isValid= true;
              $('#msg_wlists').html('').hide();
              $('#msg_blists').html('').hide();
           
          }
          else if(task_type[0].checked)//探测任务
          {
            if(enegine_type=='01')//域名变换规则
            {
              if(validateChecked('wlists[]')||validateChecked('blists[]')){              
                $('#msg_wlists').html('').hide();
                isValid = true;
              }
              else{
               $('#msg_wlists').html('请至少选择一条被保护网站').show();
               $('#msg_blists').html('请至少选择一条仿冒网站').show();
              }
            }
            else//元搜索
            {
              isValid= true;
              $('#msg_wlists').html('').hide();
              $('#msg_blists').html('').hide();
            }

          }
          else//探测及验证任务
          {
              if(enegine_type=='01')//域名变换规则
              {
                if(validateChecked('wlists[]')){              
                  $('#msg_wlists').html('').hide();
                  isValid = true;
                }
                else
                  $('#msg_wlists').html('请至少选择一条被保护网站').show();
            }
              else//元搜索
              {
                isValid= true;
                $('#msg_wlists').html('').hide();
                $('#msg_blists').html('').hide();
              }



            
              
          }
          
        return isValid;
      }  
    //checkbox至少选一项
       function validateChecked(name){
         var top = document.getElementsByName(name);
         var isValid = false;
            for(i=0; i<top.length; i++) {
            if(top[i].checked) {
                isValid = true;

                 break;
                 }

            }
            return isValid;
      } 
       
      
      
     
       
       
    
    

        
</script>
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
                        <li><a href="__APP__/Task/task_index.html"> 查看任务</a></li>
                        <li class = "active"><a href="__APP__/Task/task_add.html"> 添加任务</a></li>
                       
                        <li><a href="__APP__/Task/task_result.html"> 查看已完成任务结果</a></li>
                        
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
    <div class="main-content" >

       
        <div class="page-heading">
            
            <ul class="breadcrumb">
                 <li><a href="__APP__/Index/indexMain.html">首页</a></li>
                <li>
                    <a href="#">任务管理</a>
                </li>
                <li class="active"> 添加任务 </li>
            </ul>
        </div>
        <!-- page heading end-->

        <!--body wrapper start-->
        <section class="wrapper">
        <!-- page start-->


        <div class="row">
            <div class="col-lg-12" >
                <section class="panel">
                    <header class="panel-heading">
                        添加任务
                    </header>
                    <div class="panel-body" > 
                        <table align="center" border="0" cellpadding="0" cellspacing="0">
                          <tr><td>

 
                          <form class="cmxform form-horizontal adminex-form" id="taskForm" method="post" action=<?php echo U('Task/task_add_action');?>  >  
                            <input type='hidden' name="issubmit" value="1">
                    <!-- Tabs -->
                            <div id="wizard" class="swMain">
                                <ul>
                                    <li><a href="#step-1">
                                    <label class="stepNumber">1</label>
                                    <span class="stepDesc">
                                       选择任务类型<br />
                                       
                                    </span>
                                </a></li>
                                    <li><a href="#step-2">
                                    <label class="stepNumber">2</label>
                                    <span class="stepDesc">
                                       选择任务配置文件<br />
                                      
                                    </span>
                                </a></li>
                                    <li><a href="#step-3">
                                    <label class="stepNumber">3</label>
                                    <span class="stepDesc">
                                       选择任务检测名单<br />
                                       
                                    </span>
                                 </a></li>
                                   
                                </ul>
                                <div id="step-1">   
                                 <h2 class="StepTitle">Step 1:任务类型</h2>
                             
                                        <div class="form-group " >
                                        </div>
                                        <div class="form-group"   >
                                            <label for="cname" class="control-label col-lg-2">名称</label>
                                                            <div class="col-lg-5">
                                                                <input class=" form-control" id="taskname"  size="16"name="taskname" minlength="2" type="text" required />
                                                                <span id="msg_taskname"></span>&nbsp;

                                                            </div>
                                                               
                                        </div>
                                       
                                            
                                        <div class="form-group"   >
                                          <label class="col-sm-2 control-label col-lg-2" for="inputSuccess">选择任务类型</label>
                                            <div class="col-lg-10">
                                                <label>
                                                  <input type="radio" name="tasktype" id="tasktype" value="1"  onclick="switchRadio(1)">探测任务</label>
                                                  <label>
                                                  <input type="radio" name="tasktype" id="tasktype" value="2"  onclick="switchRadio(3)">验证任务</label>
                                                  <label>
                                                  <input type="radio" name="tasktype" id="tasktype" value="3" onclick="switchRadio(2)"checked>探测及验证任务</label>
                                                            
                                                             
                                                               
                                                            
                                                               

                                            </div>
                                          </div>
                                             <div class="form-group"   >
                                                                <label class="col-sm-2 control-label col-lg-2" for="inputSuccess">选择探测任务引擎</label>
                                                            <div class="col-lg-10">
                                                                <select id="engine" name="engine" class="txtBox">
                                                                     <option value="0">-select-</option>
                                                                     <option value="01" >域名变换探测引擎</option>
                                                                     <option value="02" >元搜索敏感信息探测引擎</option>   
                                                                     <option value="03" >微博敏感信息探测引擎</option>  
                                                                     

                                                                 </select>
                                                                 <span id="msg_taskengine"></span>&nbsp;
                                                               </div>
                                                                
                                              </div>
                                                      
                                        <div class="form-group" id="task1">
                                           <label class="col-sm-2 control-label col-lg-2" for="inputSuccess">选择验证任务引擎</label>
                                                <div class="col-lg-10">
                                                    <label class="checkbox-inline">
                                                        <input type="checkbox" name="engine1[]" id="engine1" value="08" > 网页关键字比对引擎
                                                    </label>
                                                                
                                                    <label class="checkbox-inline">
                                                        <input type="checkbox"name="engine1[]" id="engine1" value="09" > 网页结构比对引擎
                                                    </label>
                                                                
                                                    <label class="checkbox-inline">
                                                        <input type="checkbox" name="engine1[]"id="engine1" value="10" > 网页视觉身份特征比对引擎
                                                    </label>
                                                    <span id="msg_taskengine1"></span>&nbsp;

                                                </div>
                                        </div>
                                                       
                                        <div class="form-group"></div>
                                        <div class="form-group"></div>
                                </div>
                                <div id="step-2">
                                 <h2 class="StepTitle">Step 2: 选择配置文件</h2>  
                                  
                                  <div class="form-group" id="changerules"  >
                                    
                                          <div class="col-sm-3">
                                              <section class="panel">
                                        
                                                  <div class="panel-body">
                                                    <table class="table">
                                                    <thead>
                                                    <tr>
                                                        <th><input type="checkbox" onclick="selectAll('toprules[]','selectedt')" id ="selectedt"/></th>
                                                        
                                                         <th>顶级域名变换规则</th>
                                                        
                                                    </tr>
                                                    </thead>
                                                    <tbody>
                                                <?php if(is_array($toprule)): $i = 0; $__LIST__ = $toprule;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                                    <td><input type="checkbox" id="toprules"  name = "toprules[]" value = "<?php echo ($one["id"]); ?>"  /></td>
                                                         <td><?php echo ($one["change_rule"]); ?></td>
                                                        
                                       
                                                    </tr><?php endforeach; endif; else: echo "" ;endif; ?> 
                                                    <span id="msg_toprules"></span>&nbsp;
                                                    </tbody>
                                                </table>
                                               </div>
                                              </section>
                                          </div>
                                          <div class="col-sm-6">
                                            <section class="panel">
                                        
                                                <div class="panel-body">
                                                  <table class="table">
                                                      <thead>
                                                      <tr>
                                                          <th><input type="checkbox" onclick="selectAll('urlrules[]','selectedu')" id = "selectedu" group="urlrules" /></th>
                                                          <th>主机域名变换规则</th>
                                                          <th>备注</th>
                                                          
                                                      </tr>
                                                      </thead>
                                                      <tbody>
                                                  <?php if(is_array($urlrule)): $i = 0; $__LIST__ = $urlrule;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                                      <td><input type="checkbox" id = "urlrules" name = "urlrules[]" value = "<?php echo ($one["id"]); ?>" /></td>
                                                          
                                                            <td><?php echo ($one["change_rule"]); ?></td>
                                                           <td><?php echo ($one["node"]); ?></td>
                                         
                                                      </tr><?php endforeach; endif; else: echo "" ;endif; ?> 
                                                      <span id="msg_urlrules"></span>&nbsp;
                                                      </tbody>
                                                  </table>
                                                </div>
                                            </section>
                                          </div>
                                          <div class="col-sm-3">
                                            <section class="panel">
                                                <div class="panel-body">
                                                  <table class="table">
                                                      <thead>
                                                      <tr>
                                                          <th><input type="checkbox" onclick="selectAll('pathrules[]','selectedp')" id = "selectedp" group="pathrule[]" /></th>
                                                         
                                                           <th>路径变换规则   </th>
                                                          
                                                      </tr>
                                                      </thead>
                                                      <tbody>
                                                  <?php if(is_array($pathrule)): $i = 0; $__LIST__ = $pathrule;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                                      <td><input type="checkbox" id="pathrules" name = "pathrules[]" value = "<?php echo ($one["id"]); ?>" /></td>
                                                           
                                                           <td><?php echo ($one["change_rule"]); ?></td>
                                         
                                                      </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                                                      <span id="msg_pathrules"></span>&nbsp; 
                                                      </tbody>
                                                  </table>
                                              </div>
                                            </section>
                                          </div>
                                           
                                  </div>

                                      
                                   
                                  <div class="form-group" id="keywords">
                                      <div class="col-sm-5" align = "center">
                                          <section class="panel">
                                          
                                              <div class="panel-body">
                                                <table class="table">
                                                    <thead>
                                                    <tr>
                                                        <th><input type="checkbox" onclick="selectAll('kwords[]','selectedk')" id="selectedk" /></th>
                                                        <th>敏感关键字</th>
                                                        
                                                    </tr>
                                                    </thead>
                                                    <tbody>
                                                    <?php if(is_array($kword)): $i = 0; $__LIST__ = $kword;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                                    <td><input type="checkbox" id="kwords" name = "kwords[]" value = "<?php echo ($one["id"]); ?>"  /></td>
                                                         <td><?php echo ($one["sensitive_word"]); ?></td>
                                       
                                                    </tr><?php endforeach; endif; else: echo "" ;endif; ?> 
                                                    <span id="msg_kwords"></span>&nbsp;
                                                    </tbody>
                                                </table>
                                              </div>

                                          </section>
                                      </div>             
                                  </div>  


                                   
                                  <div class="form-group" id="suspectedlist">    
                                     
                                
                                      <div class="col-lg-12">
                                          <section class="panel" id="gray_list">
                                            <div class="panel-body">  
                                                <div class="adv-table" >
                                                    <table class="table table-striped table-hover table-bordered" id="editable-sample">
                                                        <thead>
                                                          <tr>
                                                             <th width="20%"><input type="checkbox" class="checkboxCtrl" group ="ids" onclick="selectAll('blists[]','selectedg')" id = "selectedg"/></th> <th width="20%">仿冒网站黑名单URL</th>                      
                                                              </tr>
                                                          </thead>              
                                                          <tbody>                     
                                                            <?php if(is_array($gray)): $i = 0; $__LIST__ = $gray;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                                                <td><input type="checkbox" id="grayids" name = "grayids[]" value = "<?php echo ($one["id"]); ?>" /></td>
                                                                 <td><?php echo ($one["url"]); ?></td>
                                                                                     
                                                              </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                                                         </tbody>
                                                          <span id="msg_slists"></span>&nbsp;
                                                      </table>
                                                </div>
                                            </div>
                                          </section>
                                       </div>
                                                                

                                </div>
                                </div>                      
                                <div id="step-3">
                                  <h2 class="StepTitle">Step 3: 选择待检测名单</h2>  
                                   <div class="form-group" >  

                                   </div>
                                   <div class="form-group" >
                                      <label class="col-sm-2 control-label col-lg-4" for="inputSuccess" id ="detectedMessage">选择检测名单类型</label>
                                        <div class="col-lg-6">
                                          <label>
                                            <input type="radio" name="detecttype" id="protected_choose" value="1"  onclick="controlTable(1)"checked>被保护网站白名单</label>
                                            <label>
                                             <input type="radio" name="detecttype" id="counterfeit_choose" value="2" onclick="controlTable(2)">仿冒网站黑名单</label>
                                        </div>
                                  </div>
                                   
                                  <div class="form-group" id="task2">                                        
                                      <div class="col-lg-12">
                                                <section class="panel" id="protected_list">         
                                                    <div class="panel-body">
                                                        
                                                          <div class="adv-table" >
                                                              <table  class="display table table-bordered table-striped" >
                                                                      <thead>
                                                                        <tr>
                                                                          <th>被保护网站URL</th>
                                                                          <th>被保护网站名称</th>
                                                                          <th><input type="checkbox" class="checkboxCtrl" group ="ids" onclick="selectAll('wlists[]','selectedw')" id = "selectedw"/></th>
                               
                                                                        </tr>
                                                                      </thead>
                                                                      <tbody>
                                                                        <?php if(is_array($wlist)): $i = 0; $__LIST__ = $wlist;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                                                            <td><?php echo ($one["url"]); ?></td>
                                                                            <td><?php echo ($one["website_name"]); ?></td>
                                                                            <td><input type="checkbox" id="wlists" name = "wlists[]" value = "<?php echo ($one["id"]); ?>" /></td>
                                                                           </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                                                                      </tbody>
                                                                      <span id="msg_wlists"></span>&nbsp;
                                                                    </table>
                                                          </div>       
                                                        
                                                    </div>
                                                 </section>
                                      </div>
                                      <div class="col-lg-12">
                                          <section class="panel" id="counterfeit_list">
                                            <div class="panel-body">  
                                                <div class="adv-table" >
                                                    <table class="table table-striped table-hover table-bordered" id="editable-sample">
                                                                        <thead>
                                                                          <tr>
                                                                            
                                                                            
                                                                            <th width="20%"><input type="checkbox" class="checkboxCtrl" group ="ids" onclick="selectAll('blists[]','selectedb')" id = "selectedb"/></th> <th width="20%">仿冒网站黑名单URL</th>       
                                                                                   
                                                                                   
                                                                          </tr>
                                                                         </thead>              
                                                                          <tbody>                     
                                                                         <?php if(is_array($blist)): $i = 0; $__LIST__ = $blist;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$one): $mod = ($i % 2 );++$i;?><tr>
                                                                               <td><input type="checkbox" id="blists" name = "blists[]" value = "<?php echo ($one["id"]); ?>" /></td>
                                                                              <td><?php echo ($one["url"]); ?></td>
                                                                                     
                                                                            </tr><?php endforeach; endif; else: echo "" ;endif; ?>
                                                                          </tbody>
                                                      </table>
                                                </div>
                                            </div>
                                          </section>
                                       </div>
                                   </div>

                                  
                                   <div class="form-group" >  
                                   </div>
                                                                   
                                </div>
                                
                            </div>
                          <!-- End SmartWizard Content -->        
                        </form> 
        
                        </td></tr>
                      </table> 
                    </div>
                </section>
            </div>
         </div>
        
        
        <!-- page end-->
        </section>
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
<script src="__TMPL__/js/jquery-ui-1.9.2.custom.min.js"></script>
<script src="__TMPL__/js/jquery-migrate-1.2.1.min.js"></script>
<script src="__TMPL__/js/bootstrap.min.js"></script>
<script src="__TMPL__/js/modernizr.min.js"></script>
<script src="__TMPL__/js/jquery.nicescroll.js"></script>

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
<script>


//根据选择的任务类型，使验证引擎可选或不可选，x==1:选择探测任务，不需选择验证引擎，x==2:需要选验证引擎
            function switchRadio(x) {
                var chk = document.getElementById("engine");
                var chks = document.getElementsByName("engine1[]");
                if(x==3){ 
                  chk.disabled=true;
                  for (var i = 0;i < chks.length;i ++) {
                      chks[i].disabled = false;
                      chks[i].checked = false;
                  }
                }
                else{
                  chk.disabled=false;
                  if(x==1) flag = true;
                  else flag =false;
                  for (var i = 0;i < chks.length;i ++) {
                      chks[i].disabled = flag;
                      chks[i].checked = false;


                  }
                }
           
            }

            function controlTable(x) {
                
                if(x==1){
                  $('#counterfeit_list').hide();
                  $('#protected_list').show();
                }
                else{
                  $('#protected_list').hide();
                  $('#counterfeit_list').show();
                }

                
            }
            

            
          //全选or反选checkbox，参数为控件的id和name
          
           function selectAll(name,id){
  var checklist = document.getElementsByName(name);
   if(document.getElementById(id).checked)
   {
   for(var i=0;i<checklist.length;i++)
   {
       checklist[i].checked= 1;
     
   } 
 }else{
  for(var j=0;j<checklist.length;j++)
  {
     checklist[j].checked = 0;
  }
 }
}


            
</script>

</body>
</html>