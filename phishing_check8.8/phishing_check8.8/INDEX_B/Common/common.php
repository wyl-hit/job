 <?php
function userLog($act,$user)
    {
            
            $action['time'] = date('Y-m-d H:i:s',time());
            $action['action'] = $act;
            $action['user_id'] =$user['id'];

            
            // if(get_client_ip() == '0.0.0.0')
            //     $action['user_ip'] =  gethostbyname($_ENV['COMPUTERNAME']);
            // else
               //$action['user_ip'] = get_client_ip();
            $action['user_ip'] =  gethostbyname($_ENV['COMPUTERNAME']);

           $userlog_id=M('userlog')->add($action);
           return $userlog_id;

    }
    function detection_check($id){
      $mongo = new Mongo("mongodb://172.31.159.248:27017",array('connect'=>true));
            if($mongo){
                $sum = 20;//每个灰名单里存放的url个数
                $counter_url = 0;//当前灰名单内url总数
                $count_gray = 0;//灰名单中子灰名单个数 

                $collection = $mongo->phishing_check->gray_list; //选择数据库->数据表  
                //将传来的参数生成一个mongoid对象，即灰名单的id
                $main_gray = $collection->find(array('_id' => new mongoId($id)));  //通过id查到一条记录
                
                $gray = iterator_to_array($main_gray);//将主记录转换成array格式
                $gray_array = $gray[$id]; //得到这条记录的array格式

                $gray_list = $gray_array['gray_list'];//前20个灰名单
                $child_gray_id = $gray_array['child_gray'];//当前灰名单的子灰名单id
                $array[] =array();
                for($i =0;$gray_list[$i]&&$i<$sum;$i++){
                    $array[] = $gray_list[$i];
                    $counter_url++;
                }

                

                while($child_gray_id[$count_gray]) {
                    // $child_gray = iterator_to_array(
                    //                  $collection->find(array('_id' => $child_gray_id[$count]))
                    //                  );
                    // $child_gray_array = $child_gray['gray_list'];//获得子灰名单的array
                    $child_id = $child_gray_id[$count_gray];//子灰名单id(mongdoid)
                    $child_gray = $collection->find(array('_id' => $child_id))->getNext();//通过子灰名单id得到子灰名单
                    $child_gray_list = $child_gray['gray_list'];//得到子灰名单中的灰名单url array
                    for($i =0;$child_gray_list[$i]&&$i<=$sum;$i++){
                        $array[] = $child_gray_list[$i];
                        $counter_url++;
                    }
                    $count_gray++;

                } 
                
                
                 
                vendor("Excel.PHPExcel");

                $objPHPExcel = new PHPExcel();

                $objPHPExcel->getProperties()->setCreator("Maarten Balliauw")//创建者
                                            ->setLastModifiedBy("Maarten Balliauw")//最后修改者
                                            ->setTitle("Office 2007 XLSX Test Document")//标题
                                            ->setSubject("Office 2007 XLSX Test Document")//主题
                                            ->setDescription("Test document for Office 2007 XLSX, generated using PHP classes.")//备注
                                            ->setKeywords("office 2007 openxml php")//关键字
                                            ->setCategory("Test result file");//分类
                
                $i=1;
                $objPHPExcel->setActiveSheetIndex(0)
                            ->setCellValue('A1', 'URL');//设置第一列为url 的id
                            
                            

                $objPHPExcel->setActiveSheetIndex(0);
                for($i=1;$i<=$counter_url;$i++){
                    $objPHPExcel->setActiveSheetIndex(0)
                            ->setCellValue('A'.$i, $array[$i]);
                           
                   
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
                header('Content-Disposition:attachment;filename='.date('Ymdhms').'.xls');//设置文件的名称
                header("Content-Transfer-Encoding:binary");

                $objWriter = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel5');
                
                $objWriter->save('php://output');
                //记录用户行为
                $user =session('user'); 
                $aciton = C('ACTION_OPTSLIST');
                userLog($aciton,$user);


                
                $mongo ->close();
            }
            else
              echo "<script>alert(连接数据库失败！);</script>";
    }
function newMongoDB(){
      return new Mongo("mongodb://192.168.65.148:27017",array('connect'=>true));//初始化类
}
    function sendSocket($taskid,$type){
        $condition['type']= '00'; 
        $server_live = M('server_live')->where($condition)->select();
        
        $service_port =$server_live[0]['port'];
        
        $address = $server_live[0]['ip'];
       
        $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        if ($socket === false) 
          return 'socket create failed';
        
        else 
        {
            $result = socket_connect($socket, $address, $service_port);
            if($result === false) 
                return 'socket connect failed';
         
            else 
            {
                $in = $type;
                $in .= $taskid;
                $out = '';
                socket_write($socket, $in, strlen($in));        
                while ($out = socket_read($socket, 8192)) 
                  return $out;
                
            }
       
        }

        socket_close($socket);
    }

    function template(){
         vendor("Excel.PHPExcel");

        $objPHPExcel = new PHPExcel();

        $objPHPExcel->getProperties()->setCreator("Maarten Balliauw")//创建者
                                    ->setLastModifiedBy("Maarten Balliauw")//最后修改者
                                    ->setTitle("Office 2007 XLSX Test Document")//标题
                                    ->setSubject("Office 2007 XLSX Test Document")//主题
                                    ->setDescription("Test document for Office 2007 XLSX, generated using PHP classes.")//备注
                                    ->setKeywords("office 2007 openxml php")//关键字
                                    ->setCategory("Test result file");//分类
        
        
        $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('A1', '此列填写被保护网站url/可疑网站url');//设置第二列为url
        $objPHPExcel->getSheet(0)->setTitle('被保护(可疑)网站导入表模板');//设置sheet标签的名称
      
        $objPHPExcel->createSheet();
        $objPHPExcel->setActiveSheetIndex(1)
                    ->setCellValue('A1', '此列填写被信任网站url')//设置第一列为url 的id
                    ->setCellValue('B1', '此列填写被信任网站名称');//设置第二列为url
        $objPHPExcel->getSheet(1)->setTitle('被信任网站导入表模板');//设置sheet标签的名称 

        $objPHPExcel->createSheet();
        $objPHPExcel->setActiveSheetIndex(2)
                    ->setCellValue('A1', '此列填写仿冒网站URL')//设置第一列为url 的id
                    ->setCellValue('B1', '此列填写被仿冒网站URL')
                    ->setCellValue('C1', '此列填写被仿冒网站名称');//设置第二列为url
        $objPHPExcel->getSheet(2)->setTitle('仿冒网站导入表模板');//设置sheet标签的名称    

        $objPHPExcel->createSheet();
        $objPHPExcel->setActiveSheetIndex(3)
                    ->setCellValue('A1', '例如：\.com')//设置第一列为url 的id
                    ->setCellValue('B1', '例如：.cn,.tk,.net,.org');//设置第二列为url
        $objPHPExcel->getSheet(3)->setTitle('顶级域名规则导入表模板');//设置sheet标签的名称 

        $objPHPExcel->createSheet();
        $objPHPExcel->setActiveSheetIndex(4)
                    ->setCellValue('A1', '例如：io(\d+)')//设置第一列为url 的id
                    ->setCellValue('B1', '例如：io(0--4)');//设置第二列为url
        $objPHPExcel->getSheet(4)->setTitle('主机域名规则导入表模板');//设置sheet标签的名称  

        $objPHPExcel->createSheet();
        $objPHPExcel->setActiveSheetIndex(5)
                    ->setCellValue('A1', '例如：/bank.asp');//设置第二列为url
        $objPHPExcel->getSheet(5)->setTitle('路径变换规则导入表模板');//设置sheet标签的名称  

        $objPHPExcel->createSheet();
        $objPHPExcel->setActiveSheetIndex(6)
                    ->setCellValue('A1', '此列填写关键字');//设置第一列为url 的id
                    
        $objPHPExcel->getSheet(6)->setTitle('敏感关键字导入表模板');//设置sheet标签的名称  

                      
       
        ob_end_clean();  //清空缓存 

        header("Pragma: public");
        header("Expires: 0");
        header("Cache-Control:must-revalidate,post-check=0,pre-check=0");
        header("Content-Type:application/force-download");
        header("Content-Type:application/vnd.ms-execl");
        header("Content-Type:application/octet-stream");
        header("Content-Type:application/download");
        header('Content-Disposition:attachment;filename=导入表模板.xls');//设置文件的名称
        header("Content-Transfer-Encoding:binary");

        $objWriter = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel5');
        
        $objWriter->save('php://output');
        //记录用户行为
        $user =session('user'); 
        $aciton = C('ACTION_OPTPLIST');
        userLog($aciton,$user);

        exit;   
    }

