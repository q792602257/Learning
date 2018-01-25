<?php
class inDB implements ArrayAccess{ #TODO:
	private $db_con=false;
	private $db_name=null;
	private $tables=[];
	public function __construct($con,$db_name){
		if(!$con){die('连接数据库时出现错误' . mysql_error());}
		$this->db_con=$con;$this->db_name=$db_name;
		$result = mysql_query("show tables;");
		while($arr=mysql_fetch_assoc($result)){
			;
		}
	}
	public function get_tables(){
		
	}
	public function offsetGet($offset){
	}
	public function offsetSet($offset, $value){
	}
	public function offsetExists($offset){
	}
	public function offsetUnset($offset){
	}
	public function __get($offset){
		return ($this->offsetGet($offset));
	}
	public function __set($offset, $value){
		return ($this->offsetSet($offset, $value));
	}
}
class inTABLES implements ArrayAccess{
	private $db_con=false;
	private $db_name=null;
	private $table_name=null;
	private $column=[];
	private $column_info=[];
	public function __construct($con,$db_name){
		if(!$con){die('连接数据库时出现错误' . mysql_error());}
		$this->db_con=$con;$this->db_name=$db_name;
		$result = mysql_query("show columns from $this->table_name;");
		while($arr=mysql_fetch_assoc($result)){
			array_push($this->column,$arr["Field"]);
			$this->column_info[$arr["Field"]]=$arr["Type"];
		}
	}
	public function get_tables(){
		
	}
	public function offsetGet($offset){
	}
	public function offsetSet($offset, $value){
	}
	public function offsetExists($offset){
	}
	public function offsetUnset($offset){
	}
	public function __get($offset){
		return ($this->offsetGet($offset));
	}
	public function __set($offset, $value){
		return ($this->offsetSet($offset, $value));
	}
}
class db implements ArrayAccess{
	private $_data;
	private $db_con=false;
	public function __construct($db_addr,$user,$pass){
		$db_con = mysql_pconnect($db_addr,$user,$pass);
		if(!$db_con){die('连接数据库时出现错误' . mysql_error());}
		else{$this->db_con=$db_con;}
	}
	public function offsetGet($offset){
		if(!$this->db_con){die("请连接数据库！！！");}
		$is_db=mysql_select_db($offset, $this->db_con);
		if($is_db){return new inDB($this->db_con,$offset);}else{die("提供的数据库不存在");}
	}
	public function offsetSet($offset, $value){
		if(!$this->db_con){die("请连接数据库！！！");}
	}
	public function offsetExists($offset){
		if(!$this->db_con){die("请连接数据库！！！");}
		$is_db=mysql_select_db($offset, $this->db_con);
		if($is_db){return true;}else{return false;}
	}
	public function offsetUnset($offset){
		if(!$this->db_con){die("请连接数据库！！！");}
	}
	public function __get($offset){
		return ($this->offsetGet($offset));
	}
	public function __set($offset, $value){
		return ($this->offsetSet($offset, $value));
	}
}
$a=new db("192.168.31.3:3306","root","Bd960912");
var_dump($a["mysql"]);
?>