<?php

class UserAction extends Action {
  
    public function user_index(){
    	$user =session('user'); 
    	if($user['right']){
    		 $this -> data = M('user') ->select();//从数据库中读取白名单内容
        	 $this-> action =M('userlog')->select();
        	 $this->display();
    	}
    	else {
    			echo "<script> alert('');</script>";
    			$this->redirect('Index/indexmain');

    	}
       
    }
    public function user_add(){
        $data['name'] = I('post.username');
        $data['password'] = I('post.password');
        

        $User = M('user');
        $result = $Task -> where("name = '".$data['name']."'") -> find();

        if($result == null){
            $Task -> add($data);
            //TODO: 添加操作sql结果未做检测
            $this -> ajaxReturn($Task -> getlastsql(),"添加任务成功！",1);
        }else {
            $this -> ajaxReturn($Task -> getlastsql(),"该用户名称已存在，请更改用户名称重新添加！",0);
        }

    }
    public function delete(){
        $userlog = M('userlog')->where('user_id=1')->delete();
        if($userlog){
            $user = session('user');
            $aciton = C('ACTION_DELOG');
            userLog($aciton,$user);
        }
        else
            echo "<script> alert('删除失败！');</script>";
        $this -> redirect('user_index');

    }

    public function output(){
    	vendor("Excel.PHPExcel");
    	


        $objPHPExcel = new PHPExcel();

        $objPHPExcel->getProperties()->setCreator("Maarten Balliauw")//创建者
                                    ->setLastModifiedBy("Maarten Balliauw")//最后修改者
                                    ->setTitle("Office 2007 XLSX Test Document")//标题
                                    ->setSubject("Office 2007 XLSX Test Document")//主题
                                    ->setDescription("Test document for Office 2007 XLSX, generated using PHP classes.")//备注
                                    ->setKeywords("office 2007 openxml php")//关键字
                                    ->setCategory("Test result file");//分类
        $user =session('user'); 
    	
    	
    	$userlog = M('userlog')->select();

        $i=2;
        $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('A1', '用户 id')
                    ->setCellValue('B1', '用户 ip')
                    ->setCellValue('C1', '用户操作')
                    ->setCellValue('D1', '操作时间');
                    

        $objPHPExcel->setActiveSheetIndex(0);
        foreach($userlog as $k=>$v){
            $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('A'.$i, $v['user_id'])
                    ->setCellValue('B'.$i, $v['user_ip'])
                    ->setCellValue('C'.$i, $v['action'])
                    ->setCellValue('D'.$i, $v['action_time']);
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
        header('Content-Disposition:attachment;filename=userlog'.date('Ymdhms').'.xls');//设置文件的名称
        header("Content-Transfer-Encoding:binary");

        $objWriter = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel5');
        
        $objWriter->save('php://output');

        $user =session('user'); 
        $aciton = C('ACTION_OPTLOG');
        userLog($aciton,$user);

        $this -> redirect('user_index');



    	
       
    }


}
