<?php
function conn($addr="127.0.0.1",$port=8888){
	$a=fsockopen($addr,$port);
	return $a;}
function send($a,$method,$shell=""){
	if($method=="shell"){
	$send=["method"=>$method,"shell"=>$shell];}
	else{
	$send=["method"=>$method];}
	@fputs($a,"jerryadmin".json_encode($send)."1");
	return $a;}
function read($a){
	$req="";
	if($a){
	while(!feof($a)){
	$req.=fgets($a);}}}
function handle($req){
	if(in_array(substr($req,10,1),["{","["]) && in_array(substr($req,-2,1),["}","]"])){
	$data=json_decode(substr($req,10,-1));}
	else{
	$data=substr($req,10,-1);}
	return $data;}
// shell命令返回handle(read(send(conn(),"shell",["命令名"])))
$isNginx=handle(read(send(conn(),"isNginx")));
$NginxStat=[9=>"Nginx未运行",1=>"Nginx正在运行",0=>"未安装Nginx"][$isNginx];//Nginx状态
$isMysql=handle(read(send(conn(),"isMysql")));
$MysqlStat=[9=>"Mysql未运行",1=>"Mysql正在运行",0=>"未安装Mysql"][$isMysql];//MySQL状态
$dfStat=handle(read(send(conn(),"dfStat")));
$dfBlock=$dfStat[0];//磁盘区：不显示
$dfTotal=$dfStat[1];//磁盘总大小
$dfUse=$dfStat[2];//磁盘已用大小
$dfAvail=$dfStat[3];//磁盘可用大小
$dfPercent=$dfStat[4];//百分比
$upTime=handle(read(send(conn(),"upTime")));
$upWhen=$upTime[0];//啥时候开机的
$upTotaltime=$upTime[1];//开机多久了
$users=$upTime[2];//当前在线用户
$LoadAvg1M=$upTime[3];//1分钟负载
$LoadAvg5M=$upTime[4];//5分钟负载
$LoadAvg15M=$upTime[5];//15分钟负载：不显示
$memStat=handle(read(send(conn(),"memStat")));
$memTotal=$memStat[1];//内存总量M
$memUsed=$memStat[2];//内存用量M
$memFree=$memStat[3]//可用内存M
$memBuffer=$memStat[4];//缓存：不显示
$memAvail=$memStat[5];//实际可用内存：不显示
?> 
