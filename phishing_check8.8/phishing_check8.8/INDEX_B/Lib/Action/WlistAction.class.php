<?php

class WlistAction extends Action {
  

    public function wlist_index(){

        $this -> protected_list = M('protected_list') ->select();//从数据库中读取白名单内容
        
        $this->display();
    }
   public function wlist_trusted(){
        $this -> trusted_list = M('trusted_list') ->select();//从数据库中读取白名单内容
        $this->display();
   }

    public function trusted_output(){
        vendor("Excel.PHPExcel");

        $objPHPExcel = new PHPExcel();

        $objPHPExcel->getProperties()->setCreator("Maarten Balliauw")//创建者
                                    ->setLastModifiedBy("Maarten Balliauw")//最后修改者
                                    ->setTitle("Office 2007 XLSX Test Document")//标题
                                    ->setSubject("Office 2007 XLSX Test Document")//主题
                                    ->setDescription("Test document for Office 2007 XLSX, generated using PHP classes.")//备注
                                    ->setKeywords("office 2007 openxml php")//关键字
                                    ->setCategory("Test result file");//分类
        
        
        $rs=M('trusted_list')->select();//从数据库中获得白名单中的所有url
        $i=2;
        $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('A1', 'URL id')//设置第一列为url 的id
                    ->setCellValue('B1', '被保护网站URL')//设置第二列为url
                    ->setCellValue('C1', '添加人')//设置第二列为url
                    ->setCellValue('D1', '添加时间');//设置第二列为url
                    

        $objPHPExcel->setActiveSheetIndex(0);
        foreach($rs as $k=>$v){//将数据库中的数据存入xls文件中
            $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('A'.$i, $v['url_id'])
                    ->setCellValue('B'.$i, $v['url'])
                    ->setCellValue('C'.$i, $v['add_user'])
                    ->setCellValue('D'.$i, $v['add_time']);
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
        header('Content-Disposition:attachment;filename=trustedlist'.date('Ymdhms').'.xls');//设置文件的名称
        header("Content-Transfer-Encoding:binary");

        $objWriter = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel5');
        
        $objWriter->save('php://output');
        //记录用户行为
        $user =session('user'); 
        $aciton = C('ACTION_OPTTLIST');
        userLog($aciton,$user);

        exit;   
    }
     public function trusted_delete(){
        
        $model = M('trusted_list');//获取当期模块的操作对象
        $ids = $_POST['trusted'];  
        $count = count($ids);
       
        
        if(is_array($ids)){
             $where = 'url_id in('.implode(',',$ids).')';

        }else{
            $where = 'url_id='.$ids;
        }
        
        $list=$model->where($where)->delete();
        if($list) {
            $user =session('user'); 
            $aciton = C('ACTION_DELTL');
            userLog($aciton,$user);
            $this->redirect('wlist_trusted');
        }else{

            $alert  ='请选择待删除项！';
            echo "<script> alert($alert); </script>"; 
           
            $this->redirect('wlist_trusted');
           
        }
       
        
    }
    
   
    public function protected_delete() {
        
        $model = M('protected_list');//获取当期模块的操作对象
        $ids = $_POST['ids'];  
        $count = count($ids);
        
        
        if(is_array($ids)){
             $where = 'id in('.implode(',',$ids).')';

        }else{
            $where = 'id='.$ids;
        }
        
        $list=$model->where($where)->delete();
        
        if($list!==false) {
            $user =session('user'); 
            $aciton = C('ACTION_DELPL');
            userLog($aciton,$user);
         
            $this->redirect('wlist_index');
        }else{

            $alert  ='请选择待删除项！';
            echo "<script> alert($alert); </script>"; 
           
            $this->redirect('wlist_index');
           
        }
       
       
    }
    public function protected_output(){
        vendor("Excel.PHPExcel");

        $objPHPExcel = new PHPExcel();

        $objPHPExcel->getProperties()->setCreator("Maarten Balliauw")//创建者
                                    ->setLastModifiedBy("Maarten Balliauw")//最后修改者
                                    ->setTitle("Office 2007 XLSX Test Document")//标题
                                    ->setSubject("Office 2007 XLSX Test Document")//主题
                                    ->setDescription("Test document for Office 2007 XLSX, generated using PHP classes.")//备注
                                    ->setKeywords("office 2007 openxml php")//关键字
                                    ->setCategory("Test result file");//分类
        
        $rs=M('protected_list')->select();//从数据库中获得白名单中的所有url
        $i=2;
        $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('A1', 'URL')//设置第一列为url 的id
                    ->setCellValue('B1', '被保护网站名称')//设置第二列为url
                    ->setCellValue('C1', '添加人')//设置第二列为url
                    ->setCellValue('D1', '添加时间');//设置第二列为url
                    

        $objPHPExcel->setActiveSheetIndex(0);
        foreach($rs as $k=>$v){//将数据库中的数据存入xls文件中
            $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('A'.$i, $v['url'])
                    ->setCellValue('B'.$i, $v['website_name'])
                    ->setCellValue('C'.$i, $v['add_user'])
                    ->setCellValue('D'.$i, $v['add_time']);
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
        header('Content-Disposition:attachment;filename=protectedList'.date('Ymdhms').'.xls');//设置文件的名称
        header("Content-Transfer-Encoding:binary");

        $objWriter = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel5');
        
        $objWriter->save('php://output');
        //记录用户行为
        $user =session('user'); 
        $aciton = C('ACTION_OPTPLIST');
        userLog($aciton,$user);

        exit;   
    }
 public function wlist_add(){
       
        $this->display();
    }
   
   //添加白名单（仅支持上传xls文件）
	public function addWlist(){
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
        if($config == '1')//若添加的是被保护网站白名单
        {
                $tb_name = 'protected_list';
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
            $this->redirect('Wlist/wlist_index');
        else 
            $this->redirect('Wlist/wlist_trusted');
        
	}

    public function download_template(){
        template();

    }
    public function addProtected(){
        $time =date("Y-m-d H:i:s",time());
        $user =session('user'); 
        $newProtected =array(
            'url' => I('website'),
            'website_name' =>I('name'),
            'add_time'=>$time,
            'add_user'=>$user['name'],
         );
        
         $pid = M('protected_list')->add($newProtected);
        $newTask = array(
            'user_id'=>$user['id'],
            'protected_id'=>$pid,
            'task_name' => 'addProtected',
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
        

        
        $this->redirect('Wlist_index');
           


    }
      public function updateInfo()
    {
      $id=$_POST['id'];
      $user = session('user');
      $time =date("Y-m-d H:i:s",time());

      $newTask = array(
        'user_id'=>$user['id'],
        'protected_id'=>$id,
        'task_name' => 'updateProtected',
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
                $this -> ajaxReturn(1,'任务启动成功！',1);
            
       else{
            
            M('task_result')->delete($new);
            M('task_info')->delete($tid);
             $this -> ajaxReturn(0,'任务启动失败！',0);
       }

       } 
    }
    public function checkDetail($id)
    {
      $condition['id']= $id;
      $url=M('protected_list')->where($condition)->getField('url');
      $con['url'] = $url;
      $feature = M('protected_feature')->where($con)->select();
      
     
      
      if($feature){
        $feature[0]['webpage']=C('ADDRESS_PRE').$feature[0]['webpage'];
        $feature[0]['blockpage']=C('ADDRESS_PRE').$feature[0]['blockpage'];
       // var_dump($feature);
       //  $this->display('test');
       $this-> protected_feature = $feature;
       $this->display('wlist_detail');
      }
      
      else{
        echo "<script> alert('该网站暂无详情');</script>";
        $this->redirect('wlist_index');

    }

                 

    }

                

      

    
	
}



    
    

