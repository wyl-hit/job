<?php

class BlistAction extends Action {
   public function index()
   {
      $type=array();
    	$this-> country = M('counterfeit_statistic')->select();

      $result = M('protected_type') ->select();
      $type_string='';
      
      $type_string = $result[0]['type'].'/'.$result[1]['type'];

      $this -> type = explode('/', $type_string);

      $this-> source = M('counterfeit_source')->select();
      $sql = 'select s.source_name,s.type,c.id,c.source_id,c.discover_way,c.discover_time,c.url
              from counterfeit_list c,counterfeit_source s where c.source_id = s.id';
        
      $this-> data = M('counterfeit_list')->query($sql);
      
      $this -> display();
   }

   public function whois_index(){
    $this-> whois = M('whois_reverse')->limit(25)->select();
    $this->display();
   }
    public function blist_source(){
    $this-> source = M('counterfeit_source')->limit(50)->select();
    $this->display();
   }
    public function whois_contact(){
    $this-> whois = M('whois_contacts')->limit(50)->select();
    $this->display();
   }
    public function whois_domain(){
    $this-> whois = M('whois_domain')->limit(50)->select();
    $this->display();
   }
    public function blist_model()
   {

      $sql = 'select s.source_name,s.type,c.id,c.template_num,c.url
              from counterfeit_template c,counterfeit_source s 
              where c.source_id = s.id';
        
      $this-> data = M('counterfeit_template')->query($sql);
     
      $this -> display();
   }

    public function download_template(){
        template();

    }
   public function addCounterfeit(){
   
        $source = I('source_website');
        $time =date("Y-m-d H:i:s",time());
        $user =session('user'); 
        
        
        //如果选择已有源网站
        if($source)
        {
            $newCounterfeit = array(
            
                'url' => I('urlid'),
                'discover_way' => 'maunul',
                'discover_time' => $time,
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
            
                'url' => I('urlid'),
                'discover_way' => $url[0]['source'],
                'source_id' => $sourceid,
                'comment' => I('comment')?I('comment'):'',

            );
            //$cid=M('counterfeit_list')->add($newCounterfeit);

        }
        

       if($cid){
           

            //启动5号任务
             $newTask=array(
                'user_id' => $user['id'],
                'task_name' => 'addCounterfeit',
                'task_type' => 5,
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
          }

      
      
      $this -> redirect('index');
   }

   public function addAction()
   {
	
	  if(!empty($_FILES))
     {
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
        
        $tb_name = 'counterfeit_list';
        $sheet_count =0;
        while($sheet_count<2){
         
          $objPHPExcel->setActiveSheetIndex($sheet_count);
          $sheet=$objPHPExcel->getSheet($sheet_count);
          $rowCount=$sheet->getHighestRow();//excel行数
        
        for ($i = 2; $i <= $rowCount; $i++){
           $item_type['source_name']=$sheet->getCell("A".$i)->getValue(); //获取wurl的值
           $source_type = M('counterfeit_source')->where($item_type)->getField('id');
           if($source_type)//如果找到了
            {
              $item['source_id'] = $source_type;
              
            }
            else{
              $item_type['type']=$sheet->getTitle(); //获取wurl的值
              $source_type= M('counterfeit_source')->add($item_type);
              $item['source_id'] = $source_type;
            }
             
          
              
            
            $url=$item['url']=$sheet->getCell("C".$i)->getValue();  
            
            $item['hash']=md5($url);  //获取wurl的值
            $item['discover_time']=gmdate("Y-m-d", PHPExcel_Shared_Date::ExcelToPHP($sheet->getCell("E".$i)->getValue()));   
            $item['discover_way'] = 'third_party';
            $item['type']=$sheet->getTitle();
            $item['ip']=$sheet->getCell("D".$i)->getValue(); //获取wurl的值
            $item['country']=$sheet->getCell("F".$i)->getValue(); //获取wurl的值
            $item['comment']=$sheet->getCell("B".$i)->getValue(); //获取wurl的值
           

            M($tb_name)->add($item);//添加到数据库
         }
         $sheet_count++;



        } 
        $sql_clean ="TRUNCATE `counterfeit_statistic`";
        $sql_add="  INSERT INTO counterfeit_statistic (country, count)
                      SELECT
                        country,
                        count(*)
                      FROM
                         `counterfeit_list`
                      GROUP BY
                          country";
           
        M('counterfeit_statistic')->query($sql_clean);
        M('counterfeit_statistic')->query($sql_add);
        ob_end_clean();  //清空缓存 
          //记录用户行为
       

        $user =session('user'); 
        $action=C('ACTION_ADDUCH');
        userLog($aciton,$user);

        $this->redirect('Blist/index');

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


  


   public function checkResult(){

      $sql_source = 'select id from counterfeit_source where ';
      $flag=0;
      $flagL=0;
      $i=0;
      $ids='';
      if(I('type')){
        $sql_source = $sql_source.' type=\''.I('type').'\'';
        $flag=1; 
      } 
      if(I('source_website')){
        if($flag) $sql_source = $sql_source.' and source_name=\''.I('source_website').'\'';
        else{
          $sql_source = $sql_source.' source_name=\''.I('source_website').'\'';
          $flag=1;
        }

      }
      $sourceids = M('counterfeit_source')->query($sql_source);
      if($sourceids){
        for($i;$i<count($sourceids)-1;$i++)
          $ids=$ids.$sourceids[$i]['id'].',';

        $ids=$ids.$sourceids[$i]['id'];
      }

     

      $sql_list = 'select s.source_name,s.type,c.id,c.source_id,c.discover_way,c.discover_time,c.url
              from counterfeit_list c,counterfeit_source s where c.source_id = s.id';

      if(I('location')){
        $sql_list = $sql_list.' and c.country=\''.I('location').'\'';
         //选择了后两项及第一项
        if($flag==1)
           $sql_list = $sql_list.' and c.source_id in('.$ids.')'; 
      } 
      //没有选择国家
      else
      {
        //选择了类别
        if($flag==1)
           $sql_list = $sql_list.' and c.source_id in('.$ids.')'; 
      } 

     
      
      $this-> data=   M('counterfeit_list')->query($sql_list);
      $this-> country = M('counterfeit_statistic')->select();

      $result = M('protected_type') ->select();
      $type_string='';
      
      $type_string = $result[0]['type'].'/'.$result[1]['type'];

      $this -> type = explode('/', $type_string);

      $this-> source = M('counterfeit_source')->select();

     
      $this->display('index');
   }
    
    public function checkDetail($id)
    {
      $condition['id']= $id;
      $counterfeit=M('counterfeit_list')->where($condition)->limit(1)->select();
      $con['url'] = $counterfeit[0]['url'];
      $feature = M('counterfeit_feature')->where($con)->select();

     
      if($feature){
        $feature[0]['webpage']=C('ADDRESS_PRE').$feature[0]['webpage'];
        $feature[0]['blockpage']=C('ADDRESS_PRE').$feature[0]['blockpage'];

        $feature[0]['discover_time']=$counterfeit[0]['discover_time'];
        $feature[0]['discover_way']=$counterfeit[0]['discover_way'];

        $feature[0]['ip']=$counterfeit[0]['ip'];
        $feature[0]['country']=$counterfeit[0]['country'];
        $feature[0]['city']=$counterfeit[0]['city'];
        $feature[0]['comment']=$counterfeit[0]['comment'];

       
       $this-> counterfeit_feature = $feature;
      
       $this->display('blist_detail');
      }
      
      else{
        echo "<script> alert('该网站暂无详情');</script>";
        $this->redirect('index');

      }
    }
    public function updateInfo($id)
    {
      
      $user = session('user');
      $time =date("Y-m-d H:i:s",time());

      $newTask = array(
        'user_id'=>$user['id'],
        'counterfeit_id'=>$id,
        'task_type'=>4,
        'task_name' => 'updateCounterfeit',
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
       $this->ajaxReturn(1,"任务启动成功！",1);
       
     else
       $this->ajaxReturn(0,"任务启动失败！",0);
       
     }
    else
         $this->ajaxReturn(0,"任务添加失败！",0);
}
public function blist_delete(){
      $model = M('counterfeit_list');
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
            $this->redirect('index');
        }
        //否则弹出提示框
        else{

            $alert  ='请选择待删除项！';
            echo "<script> alert($alert); </script>"; 
           
            $this->redirect('index');
           
        }

    }
public function model_delete(){
      $model = M('counterfeit_template');
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
            $this->redirect('blist_model');
        }
        //否则弹出提示框
        else{

            $alert  ='请选择待删除项！';
            echo "<script> alert($alert); </script>"; 
           
            $this->redirect('blist_model');
           
        }

    }
public function checkReverse($id)
    {
      $user = session('user');
      $time =date("Y-m-d H:i:s",time());
      $con['id']=$id;


      $newTask = array(
        'user_id'=>$user['id'],
        'whois_reverse_url'=>M('counterfeit_list')->where($con)->getField('url'),
        'task_type'=>3,
        'task_name' => 'counterfeitReverse',
        'task_engine'=>'08-09-10-13',
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
       $this->ajaxReturn(1,"任务启动成功！",1);
       
     else
       $this->ajaxReturn(0,"任务启动失败！",0);
       
     }
    else
         $this->ajaxReturn(0,"任务添加失败！",0);

      
    }


    
     public function modelDetail($id)
    {
      $condition['id']= $id;
      $url=M('counterfeit_template')->where($condition)->getField('url');
      $con['url'] = $url;
      $feature = M('counterfeit_feature')->where($con)->select();
      
     
      
      if($feature){
        $feature[0]['webpage']=C('ADDRESS_PRE').$feature[0]['webpage'];
        $feature[0]['blockpage']=C('ADDRESS_PRE').$feature[0]['blockpage'];
      
       $this-> counterfeit_feature = $feature;
      
       $this->display('model_detail');
      }
      
      else{
        echo "<script> alert('该网站暂无详情');</script>";
        $this->redirect('blist_model');

      }
    }

    
}
