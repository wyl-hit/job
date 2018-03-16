<?php
use ThinkPHP\Extend\Model\MongoModel;
class SlistAction extends Action {

   
    public function whois_index(){
    
        $this -> whois = M('whois_domain')->select();
        $this -> whois_reverse = M('whois_reverse')->select();
        $this->display();
    }
     public function slist_index(){
        $this -> suspected_list = M('suspect_list')->select();
        $this -> gray_list = M('gray_list')->limit(200)->select();
        $this->display();
    }
    public function suspect_check($id,$type){
        //if($type == 2){//探测任务生成类型
          detection_check($id);
          $user =session('user'); //获得当前用户名称
          $aciton = C('ACTION_DLSLIST').$slistid;//当前动作为查看某一白名单
          userLog($aciton,$user);//调用记录用户行为的函数记录日志
          $this->display('slist_index');
        // }
        // else 



    }
     public function download_template(){
        template();

    }
  
    //删除某一白名单
    public function slist_delete(){
      
        
        $model = M('suspect_list');
        $ids = $_POST['ids'];  //获取前台勾选的url id，
        $count = count($ids);
       
        //如果$ids是一个数组即勾选的url大于一个
        if(is_array($ids)){
             $where = 'id in('.implode(',',$ids).')';//将数组拆分

        }else{
            $where = 'id='.$ids;//如果只有一个
        }
        
        $list=$model->where($where)->delete();//删除选中的url
        //如果删除成功，记录日志
        if($list!==false) {
            $user =session('user'); 
            $aciton = C('ACTION_DELPL');
            userLog($aciton,$user);
            $this->redirect('slist_index');
        }
        //否则弹出提示框
        else{

            $alert  ='请选择待删除项！';
            echo "<script> alert($alert); </script>"; 
           
            $this->redirect('slist_index');
           
        }
    } 
 	

   
   
      
 public function slist_add(){
       
        $this->display();
    }
   
   //添加白名单（仅支持上传xls文件）
	public function addSlist(){
		
         if(!empty($_FILES))//如果上传成功
        {
            $user =session('user'); 
            import('ORG.Net.UploadFile');
            $config= array(
                'allowExts' => array('xls','xlsx'),//设置上传格式
                'savePath'  => './uploads/',//设置上传文件存储路径
                'saveRule'  => 'time',
            );//配置信息

            $upload = new UploadFile($config);  
            if(!$upload->upload()){
                $this->error($upload->getErrorMsg());
            }else {
                $info = $upload->getUploadFileInfo();
            }
            
        }
        vendor("Excel.PHPExcel");

        $file_name=$info[0]['savepath'].$info[0]['savename'];
        require_once 'ThinkPHP/Extend/Vendor/Excel/PHPExcel/IOFactory.php';

     //获取excel文件
        
        $objPHPExcel = PHPExcel_IOFactory::load("$file_name");
        $objPHPExcel->setActiveSheetIndex(0);
        $sheet0=$objPHPExcel->getSheet(0);

        $rowCount=$sheet0->getHighestRow();//excel行数
  
    
       $time =date("Y-m-d H:i:s",time());
       
       
        $config = $_POST['wlist'];//选择添加配置文件类型
        if($config == '1')//若添加重点监测名单
        {
                $tb_name = 'monitor_list';
            for ($i = 0; $i <= $rowCount; $i++){
                $item['url']=$objPHPExcel->getActiveSheet()->getCell("A".$i)->getValue();  //获取wurl的值
                $item['website_name']=$objPHPExcel->getActiveSheet()->getCell("B".$i)->getValue();
                $item['add_user']=$user['name'];
                $item['add_time']=date("Y-m-d H:i:s",time());
                M($tb_name)->add($item);//添加到数据库
         
             }
                $log =  C('ACTION_ADDPL');
        }
            
        else//若添加的是信任网站名单
        {
                $tb_name = 'trusted_list';
               for ($i = 0; $i <= $rowCount; $i++){
                $URL =$item['url']=$objPHPExcel->getActiveSheet()->getCell("A".$i)->getValue();  //获取wurl的值
                $item['hash']= md5($URL);
                $item['add_user']=$user['name'];
                $item['add_time']=date("Y-m-d H:i:s",time());
                M($tb_name)->add($item);//添加到数据库
         
        }
                $log =  C('ACTION_ADDTL');
        }
         
      
       
        
        ob_end_clean();  //清空缓存 
          //记录用户行为

        
        userLog($log,$user);


        $list = $_POST['optionsRadios1'];
        if($list ==1)
            $this->redirect('Slist/monitor');
        else 
            $this->redirect('Slist/slist_index');
        
        
	}

    public function suspect_runtask(){
       $time =date("Y-m-d H:i:s",time());
       $user =session('user');
       $objectid =  $_POST['id'];

       $newTask=array(
          'task_name' =>'checkSuspected',
          'user_id' =>$user['id'],
          'task_type' =>2,
          'task_engine' => '08-09-10',
          'add_time' =>$time,
          'last_time' =>$time,

        );
       $tid = M('task_info')->add($newTask);
       if($tid){
        $newResult=array(
          'task_id' =>$tid,

          'start_time' =>$time,
          'task_state'=>'01',
           'original_grayid'=> $objectid,
          );
        $new = M('task_result')->add($newResult);

         $socketReturn = sendSocket($tid,'qr');
            
            if ($socketReturn=='succeed'){
                
               
               
                $data['info'] = '任务启动成功！';
                $data['status'] = 1;
                $data['data'] = $socketReturn;
                $aciton = C('ACTION_RUNSLIST').$tid;
                userLog($aciton,$user);
                $this -> ajaxReturn($data);
            }
            else {
                
                $condition['task_id']=$tid;
                $condition['start_time'] = $time;
                M('task_result')->where($condition)->delete();
                $this -> ajaxReturn(0,"任务启动失败!",0);
            }

       }


       
           
            
           
        
        else
            $this -> ajaxReturn(0,"此名单为手工添加，没有对应任务可以启动!",0);


    }

   

   
    //打开重点监测界面
    public function monitor(){
      $this -> monitor_list= M('monitor_list') ->select();//从数据库读出重点监测名单传到界面中
      $this->display();
    }
    //导出重点监测名单
    public function monitor_output(){

        vendor("Excel.PHPExcel");

        $objPHPExcel = new PHPExcel();

        $objPHPExcel->getProperties()->setCreator("Maarten Balliauw")//创建者
                                    ->setLastModifiedBy("Maarten Balliauw")//最后修改者
                                    ->setTitle("Office 2007 XLSX Test Document")//标题
                                    ->setSubject("Office 2007 XLSX Test Document")//主题
                                    ->setDescription("Test document for Office 2007 XLSX, generated using PHP classes.")//备注
                                    ->setKeywords("office 2007 openxml php")//关键字
                                    ->setCategory("Test result file");//分类
        
        $rs=M('monitor_list')->select();//从数据库中获得重点监测名单
        $i=2;
        $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('A1', 'URL')//设置第一列为url 的id
                    ->setCellValue('B1', '被保护网站名称')//设置第二列为url
                    ->setCellValue('C1', '添加人')//设置第二列为url
                    ->setCellValue('D1', '添加时间')//设置第二列为url
                    ->setCellValue('E1', 'ip');//设置第二列为url
                    

        $objPHPExcel->setActiveSheetIndex(0);
        foreach($rs as $k=>$v){//将数据库中的数据存入xls文件中
            $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('A'.$i, $v['url'])
                    ->setCellValue('B'.$i, $v['website_name'])
                    ->setCellValue('C'.$i, $v['add_user'])
                    ->setCellValue('D'.$i, $v['add_time'])
                    ->setCellValue('E'.$i, $v['ip']);
            $i++;
        }

        $objPHPExcel->getActiveSheet()->setTitle('sheet1');//设置sheet标签的名称
        $objPHPExcel->setActiveSheetIndex(0);
        ob_end_clean();  //清空缓存 

        header("Pragma: public");
        header("Expires: 0");
        header("Cache-Control:must-revalidate,post-check=0,pre-check=0");
        header("Content-Type:application/force-download");
        header("Content-Type:application/vnd.ms-execl");
        header("Content-Type:application/octet-stream");
        header("Content-Type:application/download");
        header('Content-Disposition:attachment;filename=monitorList'.date('Ymdhms').'.xls');//设置文件的名称
        header("Content-Transfer-Encoding:binary");

        $objWriter = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel5');
        
        $objWriter->save('php://output');
        //记录用户行为
        $user =session('user'); 
        $aciton = C('ACTION_OPTPLIST');
        userLog($aciton,$user);

        exit;   
    }
    //删除重点监测名单，前台界面勾选url
    public function monitor_delete(){
      $model = M('monitor_list');
        $ids = $_POST['ids'];  //获取前台勾选的url id，
        $count = count($ids);
       
        //如果$ids是一个数组即勾选的url大于一个
        if(is_array($ids)){
             $where = 'id in('.implode(',',$ids).')';//将数组拆分

        }else{
            $where = 'id='.$ids;//如果只有一个
        }
        
        $list=$model->where($where)->delete();//删除选中的url
        //如果删除成功，记录日志
        if($list!==false) {
            $user =session('user'); 
            $aciton = C('ACTION_DELPL');
            userLog($aciton,$user);
            $this->redirect('monitor');
        }
        //否则弹出提示框
        else{

            $alert  ='请选择待删除项！';
            echo "<script> alert($alert); </script>"; 
           
            $this->redirect('monitor');
           
        }

    }
    //删除待验证可疑灰名单
     public function gray_delete(){
      $model = M('gray_list');
        $ids = $_POST['ids'];  //获取前台勾选的url id，
        $count = count($ids);
       
        //如果$ids是一个数组即勾选的url大于一个
        if(is_array($ids)){
             $where = 'id in('.implode(',',$ids).')';//将数组拆分

        }else{
            $where = 'id='.$ids;//如果只有一个
        }
        
        $list=$model->where($where)->delete();//删除选中的url
        //如果删除成功，记录日志
        if($list!==false) {
            $user =session('user'); 
            $aciton = C('ACTION_DELPL');
            userLog($aciton,$user);
            $this->redirect('slist_index');
        }
        //否则弹出提示框
        else{

            $alert  ='请选择待删除项！';
            echo "<script> alert($alert); </script>"; 
           
            $this->redirect('slist_index');
           
        }

    }
    //查看待检测名单的详情
   public function checkDetail($id)
    {
      $condition['id']= $id;
      $gray=M('gray_list')->where($condition)->select();
      $con['url'] = $gray[0]['url'];
      $feature = M('gray_feature')->where($con)->select();
      
     
      
      if($feature){
        $feature[0]['webpage']=C('ADDRESS_PRE').$feature[0]['webpage'];
        $feature[0]['blockpage']=C('ADDRESS_PRE').$feature[0]['blockpage'];
      
       $this-> gray_feature = $feature;
       $this-> gray_result = $gray;
       
       $type_string = $result[0]['type'].'/'.$result[1]['type'];

       $this->display('slist_detail');
      }
      
      else{
        echo "<script> alert('该网站暂无详情');</script>";
        $this->redirect('slist_index');

      }
    }
    public function checkMDetail($id)
    {
      $condition['id']= $id;
      $url=M('monitor_list')->where($condition)->getField('url');
      $con['url'] = $url;
      $feature = M('monitor_feature')->where($con)->select();
      
     
      
      if($feature){
        $feature[0]['webpage']=C('ADDRESS_PRE').$feature[0]['webpage'];
        $feature[0]['blockpage']=C('ADDRESS_PRE').$feature[0]['blockpage'];
      
       $this-> gray_feature = $feature;
       
       $type_string = $result[0]['type'].'/'.$result[1]['type'];

       $this->display('monitor_detail');
      }
      
      else{
        echo "<script> alert('该网站暂无详情');</script>";
        $this -> monitor_list= M('monitor_list') ->select();//从数据库读出重点监测名单传到界面中
        $this->display('monitor');

      }
    }

     public function checkType(){
     $condition['country'] = $_POST['country'];
     
     
     $result = M('protected_type') ->where($condition)->select();
     $type = explode('/', $result[0]['type']);
     if($type){
        $data['info'] = 'ok';
        $data['status'] = count($type);
        $data['data'] = $type;

        $this -> ajaxReturn($data);
     }
     
      else 
        $this -> ajaxReturn(0,"连接数据库失败!",0);

   }

    public function checkWebsite(){


       $condition['type'] = $_POST['type'];
     
       $result = M('counterfeit_source') ->where($condition)->select();
      if($result){
        $data['info'] = 'ok';
        $data['status'] = count($result);
        $data['data'] = $result;

        $this -> ajaxReturn($data);
     }
     
      else 
        $this -> ajaxReturn(0,"连接数据库失败!",0);

   }

    public function confirmGraylist(){
        //$con['id']= $_POST['urlId'];
        $source = I('source_website');
        $con['id']=I('urlid');
        $time =date("Y-m-d H:i:s",time());
        $user =session('user'); 
        
        $gray_feature = M('gray_feature')->where($con)->select();
        $condition['url']=$gray_feature[0]['url'];
        $url=M('gray_list')->where($condition)->limit(1)->select();
        //如果选择已有源网站
        if($source)
        {
            $newCounterfeit = array(
            
                'url' => $url[0]['url'],
                'discover_way' => $url[0]['source'],
                'source_id' => $source,
                'comment' => I('comment')?I('comment'):'',

            );
            $cid=M('counterfeit_list')->add($newCounterfeit);


        }
        else{
            $newSource = array(
            
                'source_name' =>I('new_wname'),

                'source_url' =>I('new_website'),
                'type' => I('type'),

            );
            $sourceid = M('counterfeit_source')->add($newSource);
            $newCounterfeit = array(
            
                'url' => $url[0]['url'],
                'discover_way' => $url[0]['source'],
                'source_id' => $sourceid,
                'comment' => I('comment')?I('comment'):'',

            );
            $cid=M('counterfeit_list')->add($newCounterfeit);


        }
        //添加新特征
        $newFeature=array(
            'url' => $gray_feature[0]['url'],
            'add_time' => $gray_feature[0]['add_time'],
            'title' => $gray_feature[0]['title'],
            'kword' => $gray_feature[0]['kword'],
            'webpage' => str_replace(C('BREPLACE'), C('AREPLACE'), $gray_feature[0]['webpage']),
            'blockpage' => str_replace(C('BREPLACE'), C('AREPLACE'), $gray_feature[0]['blockpage']),
            'feature' => $gray_feature[0]['feature'],

        );
        $fid=M('counterfeit_feature')->add($newFeature);
        if($fid)
           M('gray_feature')->delete($con['id']);
        //删除可疑名单记录
         if($cid){
            M('gray_list')->delete($url['id']);

            //启动5号任务
             $newTask=array(
                'user_id' => $user['id'],
                'task_type' => 5,
                'task_name' => 'confirmGray',
                'counterfeit_id' => $cid,
                'add_time' => $time,
                'last_time' => $time,
             );
             $tid = M('task_info')->add($newTask);
             if($tid){
                 
              
                 $newResult = array(
                    'task_id' =>$tid,
                    'task_state' => '01',
                    'start_time' => $time,
                    );
                 $new = M('task_result')->add($newResult);
               
                
                $socketReturn = sendSocket($tid,'qr');
                
               if ($socketReturn=='succeed')
                  echo "<script>alert('任务启动成功！');</script>";
               else{
                  echo "<script>alert('任务启动失败！');</script>";
                  M('task_result')->delete($new);
                  M('task_info')->delete($tid);
                }

            }
        else
            echo "<script>alert('任务添加失败！');</script>";
        }

        $this -> suspected_list = M('suspect_list')->select();
        $this -> gray_list = M('gray_list')->limit(200)->select();
        $this->display('slist_index');
      
    }
     public function updateMInfo($id){

      
      $user = session('user');
      $time =date("Y-m-d H:i:s",time());

      $newTask = array(
        'user_id'=>$user['id'],
        'monitor_id'=>$id,
        'task_name' => 'updateMonitor',
        'task_type'=>4,
        'add_time'=> $time,
        'last_time'=>$time,
        );
      $tid = M('task_info')->add($newTask);
      if($tid){
         $newResult = array(
           'task_id' =>$tid,
           'task_state' => '01',
           'start_time' => $time,
          );
        $new = M('task_result')->add($newResult);
               
                
        $socketReturn = sendSocket($tid,'qr');
                
         if ($socketReturn=='succeed')
                  echo "<script>alert('任务启动成功！');</script>";
          else{
              echo "<script>alert('任务启动失败！');</script>";
              M('task_result')->delete($new);
              M('task_info')->delete($tid);
          }
        }

        else
            echo "<script>alert('任务添加失败！');</script>";
        

        
        $this->redirect('monitor');

     }
     public function updateInfo($id)
    {
      
      $user = session('user');
      $time =date("Y-m-d H:i:s",time());

      $newTask = array(
        'user_id'=>$user['id'],
        'gray_id'=>$id,
        'task_name' => 'updateSuspected',
        'task_type'=>4,
        'add_time'=> $time,
        'last_time'=>$time,
        );
      $tid = M('task_info')->add($newTask);
      if($tid){
         $newResult = array(
           'task_id' =>$tid,
           'task_state' => '01',
           'start_time' => $time,
          );
        $new = M('task_result')->add($newResult);
               
                
        $socketReturn = sendSocket($tid,'qr');
                
         if ($socketReturn=='succeed')
                  echo "<script>alert('任务启动成功！');</script>";
          else{
              echo "<script>alert('任务启动失败！');</script>";
              M('task_result')->delete($new);
              M('task_info')->delete($tid);
          }
        }

        else
            echo "<script>alert('任务添加失败！');</script>";
        

        $this -> suspected_list = M('suspect_list')->select();
        $this -> gray_list = M('gray_list')->limit(200)->select();
        $this->display('slist_index');
    }
    public function delete_slist(){
       
        
        $condition['id'] = $_POST['id'];
        $con['url']=M('gray_feature')->where($condition)->getField('url');
        $d =M('gray_list')->where($con)->delete();
        $f=M('gray_feature')->where($condition)->delete();
        if ($d&$f)
          $this -> ajaxReturn(1,"删除成功",1);
      
        else 
          $this -> ajaxReturn(0,"删除失败",0);
       
    }

    public function add_monitor()
    {
        $condition['id'] = $_POST['id'];
        
        $gray_feature=M('gray_feature')->where($condition)->limit(1)->select();
        $con['url'] = $gray_feature[0]['url'];
        $time =date("Y-m-d H:i:s",time());
        $user =session('user');
        
        $newMonitor= array(
                'url' => $gray_feature[0]['url'],//设置上传格式
                'add_time'  => $time ,//设置上传文件存储路径
                'add_user'  => $user['name'],
        );//配置信息


        $g=M('gray_list')->where($con)->delete();
        $m=M('monitor_list')->add($newMonitor);



        // $newFeature=array(
        //     'url' => $gray_feature[0]['url'],
        //     'add_time' => $gray_feature[0]['add_time'],
        //     'title' => $gray_feature[0]['title'],
        //     'kword' => $gray_feature[0]['kword'],
        //     'webpage' => str_replace(C('BREPLACE'), C('AMREPLACE'), $gray_feature[0]['webpage']),
        //     'blockpage' => str_replace(C('BREPLACE'), C('AMREPLACE'), $gray_feature[0]['blockpage']),
        //     'feature' => $gray_feature[0]['feature'],

        // );

        // $fid=M('monitor_feature')->add($newFeature);
        if($g&$m&$fid)
        if($g&$m&$fid)
           $this -> ajaxReturn(1,"添加成功",1);
      
        else 
          $this -> ajaxReturn(0,"添加失败",0);

        

    }

     public function addGray(){
  
        $time =date("Y-m-d H:i:s",time());
        $user =session('user'); 
        $type =$_POST['slist'];
        $newGray =array(
            'url' => I('website'),
            'add_time'=>$time,
            
         );
        //重点监测名单
        if($type ==1){
           $newGray['add_user']=$user['name'];
           $gid = M('monitor_list')->add($newGray);
           $gray_type = 'monitor_id';


        }
        //可疑灰名单
       else{
           $newGray['source']='manual';
           $gid = M('gray_list')->add($newGray);
           $gray_type = 'gray_id';


        }

        if($gid){
          $newTask = array(
              'user_id'=>$user['id'],
              'task_engine'=>implode('-', $_POST['engine1'])?implode('-', $_POST['engine1']):'',//用implode方法从页面获得checkbox的数组，得到一个字符串
              'task_name' => 'addGray',
              'task_type'=>2,
              'add_time'=> $time,
              'last_time'=>$time,
          );
          $newTask[$gray_type]=$gid;
          $tid = M('task_info')->add($newTask);
          if($tid){
               $newResult = array(
                      'task_id' =>$tid,
                      'task_state' => '01',
                      'start_time' => $time,
                      );
                   $new = M('task_result')->add($newResult);

                 
                  
                  $socketReturn = sendSocket($tid,'qr');
                  
                  if ($socketReturn=='succeed')
                  echo "<script>alert('任务启动成功！');</script>";
          else{
              echo "<script>alert('任务启动失败！');</script>";
              M('task_result')->delete($new);
              M('task_info')->delete($tid);
          }
        }

            
        else
            echo "<script>alert('任务添加失败！');</script>";
        

        
        $this->redirect('slist_index');
      }
    }

    
       
}
