<?php

class TaskAction extends Action {
  public function task_index(){
        
        // $this-> data =  M('task_info')->table('task_info info')//为两个表写别名
        //            //判断条件为信息表中在结果表中有记录即已启动，并且状态为正在运行
        //            ->field('info.task_id as task_id,info.task_name as name,info.task_type as type,
        //                     info.add_time as time,info.task_engine as engine,info.counterfeit_id as counterfeit,
        //                     info.protected_id as protected,info.gray_id as gray')//只取某几个字段，否则会取到两个表的所有字段
        //            ->Distinct(true)
        //            ->select();  
        $sql="select task_id,task_name,add_time,task_type,task_engine,protected_id,gray_id,counterfeit_id
              from task_info";
        $this-> data    = M('task_info')->query($sql);  
        $this->display();
    }


    public function task_add(){
    	//初始化
    	  $this -> wlist  = M('protected_list')->select();//从数据库取出白名单
        $this -> slist  = M('suspect_list')->select();//从数据库取出可疑名单
        $this -> gray  = M('gray_list')->select();//从数据库取出可疑名单
        $this-> kword = M('sensitive_kword')->select();
        $this-> toprule = M('top_change_rule')->select();
        $this-> pathrule = M('path_change_rule')->select();
        $this-> urlrule = M('host_change_rule')->select();
        $this-> blist = M('counterfeit_list')->limit(10)->select();
        $this->display();
    }

    public function task_add_action(){
       
       $user =session('user'); //获得当前用户名称

      $time =date("Y-m-d H:i:s",time());
      $engine = I('engine')?I('engine'):'';
     	$newTask = array( // 这里制作新增记录的值
			'task_name' => I('taskname'),    //从页面获得任务名称
      'user_id' => $user['id'],
			'task_type' => $_POST['tasktype'],   // 从页面获得白名单名称
      'task_engine' =>$engine?$engine.(implode('-', $_POST['engine1'])?'-'.implode('-', $_POST['engine1']):''):(implode('-', $_POST['engine1'])?implode('-', $_POST['engine1']):''),//用implode方法从页面获得checkbox的数组，得到一个字符串
			'gray_id' => implode('-', $_POST['grayids'])?implode('-', $_POST['grayids']):'',
      'protected_id' => implode('-', $_POST['wlists'])?implode('-', $_POST['wlists']):'',  // 从页面获得白名单名称
      'suspected_id' =>$_POST['slists']?$_POST['slists']:'',   //从页面获得灰名单名称
      'counterfeit_id' =>implode('-', $_POST['blists'])?implode('-', $_POST['blists']):'',   //从页面获得黑名单名称
      'kword_id' => implode('-', $_POST['kwords'])?implode('-', $_POST['kwords']):'',
      'path_rule_id' => implode('-', $_POST['pathrules'])?implode('-', $_POST['pathrules']):'',
      'host_rule_id' => implode('-', $_POST['urlrules'])?implode('-', $_POST['urlrules']):'',
      'top_rule_id' => implode('-', $_POST['toprules'])?implode('-', $_POST['toprules']):'',
      'add_time' => $time,
		);
    
		
		$taskid = M('task_info')->add($newTask);//添加新数据得到任务编号
    if($taskid){
        $aciton = C('ACTION_ADDTASK').$taskid;//当前动作为添加任务
        userLog($aciton,$user);//调用记录用户行为的函数记录日志
        $this->redirect('Task/task_index');
    }
    else {
      $this ->error('出现系统错误！');
    }
      
        //$this->display('test');
    }
   
    
    public function checkProcess(){

      $condition['task_id'] = $_POST['id'];
     
      $condition['start_time'] = $_POST['time'];
      $task = M('task_result');

      $result = $task ->where($condition)->select();

      if ($result){
        // $user =session('user'); //获得当前用户名称
        // $aciton = C('ACTION_TASKSTATE').$condition['task_id'] ;//当前动作为查看任务状态
        // userLog($aciton,$user);//调用记录用户行为的函数记录日志
        
        
        $data['info'] = 'ok';
        $data['status'] = 1;
        $data['data'] = $result[0];

        $this -> ajaxReturn($data);
      }
      else 
        $this -> ajaxReturn(0,"连接数据库失败!",0);
    }

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    public function task_delete($taskid){
         $condition['task_id'] = $taskid;//获得待删除白名单ID
       	 M('task_info')->where ($condition) ->delete();//实例化白名单变量，查找ID符合的对象，删除该记录
         //记录操作记录
    	  $user =session('user'); //获得当前用户名称
        $aciton = C('ACTION_DELTASK').$taskid;//当前动作为删除任务
        userLog($aciton,$user);//调用记录用户行为的函数记录日志

       $this->redirect('Task/task_index');
    } 
 
    public function task_run(){

       $time =date("Y-m-d H:i:s",time());
       $taskid =  $_POST['id'];
       
       $data['last_time'] = $time;
       $condition['task_id'] = $taskid;
       $old_last = M('task_info')->where($condition)->getField('last_time');
       //更新数据库内容
       
       $newTask = array( // 这里制作新增记录的值
        'task_id' =>$taskid,
        'start_time' =>$time,
        'task_state'=>'02',
       );
       
       M('task_info')->where($condition)->save($data);
       $new = M('task_result')->add($newTask);

        
        $socketReturn = sendSocket($taskid,'qr');
        
        if ($socketReturn=='succeed'){
            
            M('task_info')->where($condition)->save($data);
            M('task_result')->add($newTask);

            $user =session('user'); //获得当前用户名称
            $aciton = C('ACTION_STARTTASK').$taskid;//当前动作为启动任务
            userLog($aciton,$user);//调用记录用户行为的函数记录日志

            $data['info'] = '任务启动成功！';
            $data['status'] = 1;
            $data['data'] = $socketReturn;
            $this -> ajaxReturn($data);
        }
        else {
            $data['last_time']=$old_last;
            M('task_info')->where($condition)->save($data);
            $condition['start_time'] = $time;
            M('task_result')->where($condition)->delete();
            $this -> ajaxReturn(0,$socketReturn,0);
        }
        //$this->display('test');
     

    }
    public function task_stop(){
      
       $condition['task_id'] =$_POST['id'];
       $data['task_state'] = '03';
       
        $socketReturn = sendSocket($condition['task_id'],'qs');
        
        if ($socketReturn=='succeed'){
            
            M('task_result')->where($condition)->save($data);
            
            $user =session('user'); //获得当前用户名称
            $aciton = C('ACTION_STOPTASK').$condition['task_id'];//当前动作为终止任务
            userLog($aciton,$user);//调用记录用户行为的函数记录日志

            $data['info'] = "任务已停止！";
            $data['status'] = 1;
            $data['data'] = $socketReturn;
            $this -> ajaxReturn($data);
        }
        else 
            $this -> ajaxReturn(0,"任务停止失败！",0);
        //$this->display('test');
     

    }

    public function task_process(){
    
     
      //联合查询，查询两个表
     
      $this -> result = M('task_result')->limit(1)->select();
      $this->display();
     
      
    }

    public function task_result(){
       $this-> taskinfo =  M('task_info')->table('task_info info,task_result result')//为两个表写别名
                   ->where('info.task_id = result.task_id AND result.task_state = 2')//判断条件为信息表中在结果表中有记录即已启动，并且状态为正在运行
                   ->field('info.task_id as id,info.task_name as name,info.task_type as type,info.last_time as time')//只取某几个字段，否则会取到两个表的所有字段
                   ->Distinct(true)
                   ->select();
      $this -> task = M('task_result')->where('task_state=3')->select();
      $this -> task_fail = M('task_result')->where('task_state=0')->select();
      $this -> result = M('task_result')->limit(1)->select();
      $this->display();
    }
    public function findResult(){
      
      $condition['task_id'] = $_POST['id'];
      $condition['start_time'] = $_POST['time'];
      $result = M('task_result') ->where($condition)->select();
     
      if ($result){

        $user =session('user'); //获得当前用户名称
        $aciton = C('ACTION_TASKRESULT').$condition['task_id'];//当前动作为查看任务结果
        userLog($aciton,$user);//调用记录用户行为的函数记录日志
        $t = $result[0];
        $data['info'] = 'ok';
        $data['status'] = 1;
        $data['data'] = $result[0];

        $this -> ajaxReturn($data);
      }
      else 
        $this -> ajaxReturn(0,"接受失败!",0);
     }

     public function show($objectid){
     
       $mongo = new Mongo("mongodb://172.31.159.248:27017",array('connect'=>true));
       if($mongo){ 
                $count = 0;//针对每个被保护网站的任务数量
                $flag=0;

                $collection = $mongo->test->domain_change; //选择数据库->数据表 
                $iterator = $collection->find();
                $c = iterator_to_array($iterator);
                $note =$c[$objectid]['exist_note'];
                  
                while($note[$count]){

                    $date[] = $note[$count]['changed_time'];
                    
                    
                    if($note[$count]['exist_changed_list']){
                      $flag= $count;
                      $num[]=$note[$count]['exist_changed_num'];
                    }
                    else {

                      $num[]=$note[$flag]['exist_changed_num'];
                    }
                    

                    $count++;
                  }
                  
                  
                  $array[0]=$date;
                  $array[1]=$num;


                 
         $this -> ajaxReturn($array,"获取分析数据成功！",1);        
      }

      else 
        $this -> ajaxReturn($array,"获取分析数据失败！",0);
      
     }

    public function download($id){
       $mongo = new Mongo("mongodb://172.31.159.248:27017",array('connect'=>true));
       if($mongo){ 
                $count = 0;//针对每个被保护网站的任务数量
                $flag=0;

                $collection = $mongo->test->domain_change; //选择数据库->数据表 
                $iterator = $collection->find();
                $c = iterator_to_array($iterator);
                $note =$c[$id]['exist_note'];
                  
                while($note[$count]){

                    $date[] = $note[$count]['changed_time'];
                    $gray[]=$note[$count]['gray_ID'];
                    
                    if($note[$count]['exist_changed_list']){
                      $flag= $count;
                      $host[] = $note[$count]['host_rule_list'];
                      $url[]= $note[$count]['exist_changed_list'];
                      $top[] = $note[$count]['top_rule_list'];
                      $path[]=$note[$count]['path_rule_list'];
                      $num[]=$note[$count]['exist_changed_num'];

                    }
                    else {
                      $host[] = $note[$flag]['host_rule_list'];
                      $url[]= $note[$flag]['exist_changed_list'];
                      $top[] = $note[$flag]['top_rule_list'];
                      $path[]=$note[$flag]['path_rule_list'];
                      $num[]=$note[$flag]['exist_changed_num'];
                    }
                    

                    $count++;
                  }
                  
                  
                  $array[0]=$date;
                  $array[1]=$num;
                  $array[2]=$url;
                  $array[3]=$host;
                  $array[4]=$top;
                  $array[5]=$path;
                  $array[6]=$gray;

                  var_dump($array[6]);

                   vendor("Excel.PHPExcel");

        $objPHPExcel = new PHPExcel();

        $objPHPExcel->getProperties()->setCreator("Maarten Balliauw")//创建者
                                    ->setLastModifiedBy("Maarten Balliauw")//最后修改者
                                    ->setTitle("Office 2007 XLSX Test Document")//标题
                                    ->setSubject("Office 2007 XLSX Test Document")//主题
                                    ->setDescription("Test document for Office 2007 XLSX, generated using PHP classes.")//备注
                                    ->setKeywords("office 2007 openxml php")//关键字
                                    ->setCategory("Test result file");//分类
        
        
       
        $i=2;
        //url，主机，路径，顶级变换规则的数量
        $count_task=0;//当前任务数
        $count_url=$count_host=$count_path=$count_top=0;
        $max=0;
        $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('A1', '任务启动时间')//设置第一列为url 的id
                    ->setCellValue('B1', '存活URL')//设置第二列为url
                    ->setCellValue('C1', '主机域名变换规则')//设置第二列为url
                    ->setCellValue('D1', '顶级域名变换规则')//设置第二列为url
                    ->setCellValue('E1', '路径变换规则')
                    ->setCellValue('F1', '可疑名单ID');//设置第二列为url
                    

        $objPHPExcel->setActiveSheetIndex(0);
        while($count_task<$count){
            $objPHPExcel->setActiveSheetIndex(0)->setCellValue('A'.$i, $array[0][$count_task])
                                                  ->setCellValue('F'.$i, $array[6][$count_task]);           ;//任务启动时间
            //将URL放入表格中的第二列
            while($array[2][$count_task][$count_url]){
                $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('B'.($i+$count_url), $array[2][$count_task][$count_url]);
                $count_url++;  
            }
            if($count_url > $max) $max=$count_url ;//取得占行数最大值

            while($array[3][$count_task][$count_host]){
                $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('C'.($i+$count_host), $array[3][$count_task][$count_host]);
                $count_host++;  
            }  
            if($count_host > $max) $max=$count_host;//取得占行数最大值 

            while($array[4][$count_task][$count_top]){
                $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('D'.($i+$count_top), $array[4][$count_task][$count_top]);
                $count_top++;  
            }  
            if($count_top > $max) $max=$count_top;//取得占行数最大值 

            while($array[5][$count_task][$count_path]){
                $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('E'.($i+$count_path), $array[5][$count_task][$count_path]);
                $count_path++;  
            }  
            if($count_path > $max) $max=$count_path;//取得占行数最大值 

            $count_url=$count_host=$count_path=$count_top=0;
            $i =$i+$max+1;
            $count_task++;
     
            
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

    }

    public function task_anaylse(){
        $this-> data = M('protected_url')->select();
        $this->display();      
    }

   
    



  } 
    

