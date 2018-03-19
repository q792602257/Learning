<?php
function listDir($dir) {
	static $allDirs = array();
	$dirs = glob($dir . '/*', GLOB_ONLYDIR);
	if (count($dirs) > 0) {
		foreach ($dirs as $d) $allDirs[] = $d;
	}
	foreach ($dirs as $dir) listDir($dir);
	return $allDirs;
} 
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
function create($db,$table,$argv1,$argv2)//Do a Create
{
	if (strlen($db) !== 0 && strlen($table) !== 0 && strlen($argv1) !== 0)
	{
// 		error_reporting(0);
		$cache = LinkDB();
		if ($cache['state'] == '1')
		{
			$con=$cache['con'];
			//MySQL db Link Ready
			mysql_select_db($db , $con);
			$mq="INSERT INTO `" . $table . "` (" . $argv1 . ") VALUES ('" . $argv2."')";
			$result = mysql_query($mq);
			if($result)
			{
				$state='1';
				$msg=$cache['msg'] . '--> Create OK';
			}
			else
			{
				$state='0';
				$msg=$cache['msg'] . '--> Error With Create' . mysql_error();
			}
		}
		else
		{
				$state='0';
				$msg=$cache['msg'] . '--> Not Do Create';
				//Fail Link to MySQL db
		}
	}
	else
	{
				$state='99';
				$msg='Empty Field';
				$mq="INSERT INTO `" . $table . "` " . $argv1 . " VALUES " . " " . $argv2 ;
	}	
	$return = array('state'=>$state,'msg'=>$msg,'debug'=>$mq);
	return $return;
	mysql_close($con);
}
function delete($db,$table,$argv1)
{
	if (strlen($db) !== 0 && strlen($table) !== 0 && strlen($argv1) !== 0)
	{
// 		error_reporting(0);
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
		}
	}
	else
	{
				$state='99';
				$msg='Empty Field';
				$mq="UPDATE `" . $table . "` WHERE " . $argv1 ;
	} 
	$return = array('state'=>$state,'msg'=>$msg,'debug'=>$mq);
	return $return;
	mysql_close($con);
}
$localFile=array();
foreach(listDir(".") as $dir)
{
	$localFile = array_merge_recursive(glob("{$dir}/*.jpg"),glob("{$dir}/*.png"),$localFile);
}
$dbQ=query("Images","image","url","");
$dbFile=array();
for($i=0;$i<$dbQ['count'];$i++)
{
	$dbFile[$i]=$dbQ['result'][$i]['url'];
}
print "本地文件数量： ".count($localFile)." 个\t\t数据库文件数量： ".count($dbFile)." 个\n";
$addToDB=array_diff($localFile,$dbFile);
$removeFromDB=array_diff($dbFile,$localFile);
print "需要添加 ".count($addToDB)." 条数据\t\t需要删除 ".count($removeFromDB)." 条数据\n";
foreach($addToDB as $add)
{
	create("Images","image","url",$add);
}
foreach($removeFromDB as $remove)
{
	delete("Images","image","url = '".$remove."'");
}
?>
