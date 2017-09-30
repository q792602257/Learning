<?php

function LinkDB()
{
// 	error_reporting(0);
	$con = mysql_connect("localhost","root","cc1123yhq");//////这里是数据库密码啥的
	if ($con)
	{
		return array('state'=>'1','msg'=>'DB Link OK', 'con'=>$con);
		//MySQL db Link Ready
	}
	else
	{
		return array('state'=>'0','msg'=>'Fail at Link DB' . mysql_error());
		//Fail Link to MySQL db
	}
}
function query($db,$table,$argv1,$argv2)//Do a Query
{
	if (strlen($db) !== 0 && strlen($table) !== 0 && strlen($argv1) !== 0)
	{
// 		error_reporting(0);
		$cache = LinkDB();
		if ($cache['state'] == '1' )
		{
			$con=$cache['con'];
			//MySQL db Link Ready
			mysql_select_db($db , $con);
			$mq="SELECT " . $argv1 . " FROM `" . $table . "` " . $argv2 ;
			$res = mysql_query($mq);
			$count = mysql_num_rows($res);
			if ($count)
			{
				$state='1';
				for($i=0;$i<$count;$i++)
				{
						$result[$i] = mysql_fetch_assoc($res);
				}
				$msg= $cache['msg'] . '--> Query OK';
			}
			else
			{
				$state='9';
				$msg= $cache['msg'] . '--> Query OK(With Empty Return)';
				$result="";
			}
		}
		else
		{
				$state='0';
				$count='0';
				$msg=$cache['msg'] . '--> Not Do Query';
				$result="";
				//Fail Link to MySQL db
		}
	}
	else
	{
				$state='99';
				$count='0';
				$result='';
				$msg='Empty Field';
				$mq="SELECT " . $argv1 . " FROM `" . $table . "` " . $argv2 ;
	}
	$return = array('state'=>$state,'msg'=>$msg,'debug'=>$mq,'result'=>$result,'count'=>$count);
	return $return;
	mysql_close($con);
} 
function update($db, $table, $argv1, $argv2)
{
	if (strlen($db) !== 0 && strlen($table) !== 0 && strlen($argv1) !== 0 && strlen($argv2) !== 0) {
		error_reporting(0);
		$cache = LinkDB();
		if ($cache['state'] == '1') {
			$con = $cache['con']; 
			//MySQL db Link Ready
			mysql_select_db($db, $con);
			$mq = "UPDATE `" . $table . "` SET " . $argv1 . " WHERE " . $argv2;
			$result = mysql_query($mq);
			if ($result) {
				$state = '1';
				$msg = $cache['msg'] . "--> Update OK";
			}
			else {
				$state = '0';
				$msg = $cache['msg'] . "--> Error With Update";
			}
		}
		else {
			$state = '0';
			$msg = $cache['msg'] . '--> Not Do Update'; 
				//Fail Link to MySQL db
			$mq = "UPDATE `" . $table . "` SET " . $argv1 . " WHERE " . $argv2;
		}
	}
	else {
		$state = '99';
		$msg = 'Empty Field';
		$mq = "UPDATE `" . $table . "` SET " . $argv1 . " WHERE " . $argv2;
	}
	$return = array('state' => $state, 'msg' => $msg, 'debug' => $mq);
	return $return;
	mysql_close($con);
}
function rand1()
{
	$dbQ=query("eh","eh","id,name,catagory","");
	return $dbQ["result"][rand(0,$dbQ["count"])];
}
function delete($db,$table,$argv1)
{
	if (strlen($db) !== 0 && strlen($table) !== 0 && strlen($argv1) !== 0)
	{
		error_reporting(0);
		$cache = LinkDB();
		if ($cache['state'] == '1')
		{
			$con=$cache['con'];
			//MySQL db Link Ready
			mysql_select_db($db , $con);
			$mq="DELETE FROM `" . $table . "` WHERE " . $argv1;
			$result = mysql_query($mq);
			if($result)
			{
				$state='1';
				$msg=$cache['msg'] . "--> Delete OK";
			}
			else
			{
				$state='0';
				$msg=$cache['msg'] . "--> Error With Delete";
			}
		}
		else
		{
				$state='0';
				$msg=$cache['msg'] . '--> Not Do Delete';
				//Fail Link to MySQL db
				$mq="DELETE FROM `" . $table . "` WHERE " . $argv1 ;
		}
	}
	else
	{
				$state='99';
				$msg='Empty Field';
				$mq="DELETE FROM `" . $table . "` WHERE " . $argv1 ;
	} 
	$return = array('state'=>$state,'msg'=>$msg,'debug'=>$mq);
	return $return;
	mysql_close($con);
}
if(isset($_GET["cata"])){
	if($_GET["cata"]=="m"){
		$where="and catagory='manga'";
	}
	elseif($_GET["cata"]=="w"){
		$where="and catagory='western'";
	}
	elseif($_GET["cata"]=="d"){
		$where="and catagory='doujinshi'";
	}
	elseif($_GET["cata"]=="c"){
		$where="and catagory='cosplay'";
	}
	elseif($_GET["cata"]=="i"){
		$where="and catagory='imageset'";
	}
	elseif($_GET["cata"]=="a"){
		$where="and catagory='artistcg'";
	}
	elseif($_GET["cata"]=="n"){
		$where="and catagory='non-h'";
	}
	else{
		$where="";
	}
}
$where='where resume=0 '.$where;
if(isset($_GET["re"])){
	update("Images","eh","`q`=NULL,`url`=NULL,`resume`=1"," id=".$_GET["re"]);
}
if(isset($_GET["delete"])){
	delete("Images","eh","id=".$_GET["delete"]);
	passthru("rm -rf ./eH/".$_GET["delete"]."/");
}
if(isset($_GET["no"])){
	if((int)$_GET["no"]<=$dbQ["count"]){
		$no = (int)$_GET["no"] ;
	}
}
$dbQ=query("Images","eh","id,title,catagory",$where);
$no = rand(0,$dbQ["count"]-1);
$res = $dbQ["result"][$no];
$id = $res["id"];
$name = $res["title"];
$cata = $res["catagory"];
$b = glob("eH/".$id."/*.jpg");
echo "<h1>".$name."</h1>\n<h3>".$cata."</h3>\n<p>". $no ."/".$dbQ["count"]."</p>";
echo "<div><a href=\"eh.php?delete=".$id."\">Let Me Die</a><span style='width:60px;'></span><a href=\"eh.php?re=".$id."\">Re:Download</a></div>";
for($i=1;$i<=count($b);$i++){
	echo "<img src=\"eH/".$id."/".$i.".jpg\" />\n";
}

?> 
