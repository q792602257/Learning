<?php
class inDB implements ArrayAccess{
	private $db_con=false;		
	public function __construct($con){
		
	}
}
class db implements ArrayAccess{
	private $_data;
	private $db_con=false;
	public function __construct($db_addr,$user,$pass){
		$db_con = mysql_connect($db_addr,$user,$pass);
		if(!$db_con){die('连接数据库时出现错误' . mysql_error());}
		else{$this->$db_con=$db_con;}
	}
	public function offsetGet($offset){
		if(!$db_con){die("请连接数据库！！！");}
		$is_db=mysql_select_db($offset, $con);
		if($is_db){return true;}else{die("提供的数据库不存在");}
	}
	public function offsetSet($offset, $value){
		if(!$db_con){die("请连接数据库！！！");}
		$this->_data[$offset] = $value;
	}
	public function offsetExists($offset){
		if(!$db_con){die("请连接数据库！！！");}
		$is_db=mysql_select_db($offset, $con);
		if($is_db){return true;}else{return false;}
	}
	public function offsetUnset($offset){
		if(!$db_con){die("请连接数据库！！！");}
		if($this->offsetExists($offset)){
			unset($this->_data[$offset]);
		}
	}
	public function __get($offset){
		return ($this->offsetExists($offset) ? $this->_data[$offset] : null);
	}
	public function __set($offset, $value){
		$this->_data[$offset] = $value;
	}
}
?>