<?php
// 本类由系统自动生成，仅供测试用途
class IndexAction extends Action {
    public function index(){
        
        $this->display('login');
    }
    public function test(){
        
        $this->display();
    }

    public function indexMain(){
        
        $this->display('index');
    }

   
    public function login(){
    	$username = I('username');
    	$pwd = I('password');
    	$user = M('user')->where(array('name'=>$username))->find();

    	if(!$user){
    		$this->error('用户不存在');
    	}
        else if ($user['password'] != $pwd){
            $this->error('密码错误');
        }
    	else{
            session('user',$user);
            $action =C('ACTION_LOGIN');
            if(userLog($action,$user)){
                $condition['id'] = $user['id'];
                M('user')->where($condition)->setField('last_logtime',date('Y-m-d H:i:s',time()));
                $this->redirect('/Index/indexMain');
            }
    		 $this->redirect('/Index/indexMain');
    	}
    }

     public function getLocationInfo(){


        $LocationInfo = M('counterfeit_statistic')->select();
       
        if($LocationInfo == null){
            //TODO: 添加操作sql结果未做检测
            $this -> ajaxReturn($LocationInfo -> getlastsql(),"获取地点信息失败！",0);
        }else {
           // $this -> ajaxReturn($result,"获取地点信息成功！",1);
            $this -> ajaxReturn($LocationInfo,"获取地点信息成功！",1);
        }

    }


   
}