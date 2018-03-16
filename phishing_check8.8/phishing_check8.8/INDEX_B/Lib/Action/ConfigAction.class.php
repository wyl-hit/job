<?php
// 本类由系统自动生成，仅供测试用途
class ConfigAction extends Action {
   public function addConfig(){
   	$this->display();
   }

 public function addConfigAction(){

    if(!empty($_FILES))//如果上传成功
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
        $objPHPExcel->setActiveSheetIndex(0);
        $sheet0=$objPHPExcel->getSheet(0);

        $rowCount=$sheet0->getHighestRow();//excel行数
        

		$config = $_POST['config'];//选择添加配置文件类型
		if($config == '1')//若添加的是主机域名变换规则
		{
				$tb_name = 'urlchange_rule';
				for ($i = 0; $i <= $rowCount; $i++){
            $item['source']=$objPHPExcel->getActiveSheet()->getCell("A".$i)->getValue();  //获取wurl的值
            $item['url_rule']=$objPHPExcel->getActiveSheet()->getCell("B".$i)->getValue();  //获取wurl的值
           
            M($tb_name)->add($item);//添加到数据库
            }
				$log =  C('ACTION_ADDUCH');
		}
			
		else if ($config == '2')//若添加的是敏感关键字
		{
				$tb_name = 'sensitive_kword';
		      for ($i = 0; $i <= $rowCount; $i++){
                $item['sensitive_word']=$objPHPExcel->getActiveSheet()->getCell("A".$i)->getValue();  //获取wurl的值
                M($tb_name)->add($item);//添加到数据库
            }
				$log =  C('ACTION_ADDKW');
		}

        else if ($config == '3')//若添加的是顶级域名变化规则
        {
                $tb_name = 'topdomain_rule';
              for ($i = 0; $i <= $rowCount; $i++){
            $item['source']=$objPHPExcel->getActiveSheet()->getCell("A".$i)->getValue();  //获取wurl的值
            $item['url_rule']=$objPHPExcel->getActiveSheet()->getCell("B".$i)->getValue();  //获取wurl的值
           
            M($tb_name)->add($item);//添加到数据库
            }
                $log =  C('ACTION_ADDKW');
        }
         else //若添加的是路径变换规则
        {
                $tb_name = 'pathchange_rule';
               for ($i = 0; $i <= $rowCount; $i++){
            
            $item['url_rule']=$objPHPExcel->getActiveSheet()->getCell("A".$i)->getValue();  //获取wurl的值
           
            M($tb_name)->add($item);//添加到数据库
            }
                $log =  C('ACTION_ADDKW');
        }
		
		

    	
   		
  
       
         
        
        ob_end_clean();  //清空缓存 
          //记录用户行为

        $user =session('user'); 
        $aciton =$log;
        userLog($aciton,$user);

        $this->redirect('Config/addConfig');
    }

   
     public function url_change(){
     	$this-> top = M('top_change_rule')->select();
        $this-> path = M('path_change_rule')->select();
        $this-> host = M('host_change_rule')->select();
        
        $this->display();
    }

    public function keyword(){
        
        $this-> data = M('sensitive_kword')->select();
        $this->display();
    }
     public function download_template(){
        template();

    }
    

    public function kword_delete(){
        $model = M('sensitive_kword');//获取当期模块的操作对象
        $ids = $_POST['kword_ids'];  
        $count = count($ids);
       
        
        if(is_array($ids)){
             $where = 'id in('.implode(',',$ids).')';

        }else{
            $where = 'id='.$ids;
        }
        
        $list=$model->where($where)->delete();
        if($list) {
            $user =session('user'); 
            $aciton = C('ACTION_DELKW').'account'.$count;
            userLog($aciton,$user);
            $this->redirect('keyword');
        }else{

            $alert  ='请选择待删除项！';
            echo "<script> alert($alert); </script>"; 
           
            $this->redirect('keyword');
           
        }
    }

    public function kword_output(){
        vendor("Excel.PHPExcel");

        $objPHPExcel = new PHPExcel();

        $objPHPExcel->getProperties()->setCreator("Maarten Balliauw")//创建者
                                    ->setLastModifiedBy("Maarten Balliauw")//最后修改者
                                    ->setTitle("Office 2007 XLSX Test Document")//标题
                                    ->setSubject("Office 2007 XLSX Test Document")//主题
                                    ->setDescription("Test document for Office 2007 XLSX, generated using PHP classes.")//备注
                                    ->setKeywords("office 2007 openxml php")//关键字
                                    ->setCategory("Test result file");//分类
        
        $rs=M('sensitive_kword')->select();//从数据库中获得白名单中的所有url
        $i=2;
        $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('A1', '敏感关键字id')//设置第一列为url 的id
                    ->setCellValue('B1', '敏感关键字');//设置第二列为url
                    
                    

        $objPHPExcel->setActiveSheetIndex(0);
        foreach($rs as $k=>$v){//将数据库中的数据存入xls文件中
            $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('A'.$i, $v['id'])
                    ->setCellValue('B'.$i, $v['sensitive_word']);
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
        header('Content-Disposition:attachment;filename=sensitivekword'.date('Ymdhms').'.xls');//设置文件的名称
        header("Content-Transfer-Encoding:binary");

        $objWriter = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel5');
        
        $objWriter->save('php://output');
        //记录用户行为
        $user =session('user'); 
        $aciton = C('ACTION_OPTKW');
        userLog($aciton,$user);

        exit;   
    }

   

}