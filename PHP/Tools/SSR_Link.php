<?php
$con = mysql_connect("localhost","root","Bd960912");
if (!$con){
    die('Could not connect: ' . mysql_error());
}
mysql_select_db("jerry", $con);

function sql_ssr_get($flag,$group,$max){
    global $con;
    $ret="";
    $sql="select `server`,`port`,`protocol`,`method`,`obfs`,`keys`,`name`,`obfsparam`,`protoparam` from `ssr` WHERE";
    if ($flag!=9){
        $sql.=" `isKey`='$flag' AND ";
    }
    $sql.=" `isValid`=TRUE;";
    $result = mysql_query($sql,$con);
    if ($flag!=9 && $flag!=1){
        $need=3;
    }elseif($max!=99 && $max!=0){
        $need=$max;
    }else{
        $need=99;        
    }
    $all=mysql_num_rows($result);
    while($row = mysql_fetch_array($result)){
        $s=rand(1,$all);
        $all--;
        if ($s > $need){
            continue;
        }
        $mixed=[];
        $mixed["server"]=$row[0];
        $mixed["port"]=$row[1];
        $mixed["protocol"]=$row[2];
        $mixed["method"]=$row[3];
        $mixed["obfs"]=$row[4];
        $mixed["password"]=$row[5];
        $mixed["name"]=$row[6];
        $mixed["group"]=$group;
        $mixed["obfsparam"]=$row[7];
        $mixed["protoparam"]=$row[8];
        $ret.=ssr_link_builder($mixed)."\r\n";
        $need--;
    }
    return $ret;
}

function ssr_link_builder($mixed){
    $server=$mixed["server"];
    $port=$mixed["port"];
    $method=$mixed["method"];
    if (array_key_exists("obfs",$mixed)){
        $obfs=$mixed["obfs"];
    }else{
        $obfs="plain";
    }
    if (array_key_exists("protocol",$mixed)){
        $protocol=$mixed["protocol"];
    }else{
        $protocol="origin";
    }
    $password=$mixed["password"];
    if ($server=="" || $port=="" || $protocol=="" || $method=="" || $obfs=="" || $password==""){
        die();
    }
    $param_part=[];
    if (array_key_exists("obfsparam",$mixed)){
        $param_part["obfsparam"]=str_replace("=","",base64_encode($mixed["obfsparam"]));
    }
    if (array_key_exists("protoparam",$mixed)){
        $param_part["protoparam"]=str_replace("=","",base64_encode($mixed["obfsparam"]));
    }
    if (array_key_exists("name",$mixed)){
        $param_part["remarks"]=str_replace("=","",base64_encode($mixed["name"]));
    }
    if (array_key_exists("group",$mixed)){
        $param_part["group"]=str_replace("=","",base64_encode($mixed["group"]));
    }
    $ssr_link=$server.":".$port.":".$protocol.":".$method.":".$obfs.":".str_replace("=","",base64_encode($password))."/?";
    $ssr_link.=http_build_query($param_part);
    $ssr_link=str_replace("=","",base64_encode($ssr_link));
    $ssr_link=str_replace("+","-",$ssr_link);
    $ssr_link=str_replace("/","_",$ssr_link);
    $ssr_link="ssr://".$ssr_link;    
    return $ssr_link;
}

function ssr_link_parser($ssr_link){
    $mixed=[];
    $ssr_link=str_replace("-","+",$ssr_link);
    $ssr_link=str_replace("_","/",$ssr_link);
    $p = explode("://",$ssr_link);
    $a=base64_decode($p[1]);
    $i = explode("/?",$a);
    $server_part=explode(":",$i[0],6);
    $mixed["server"]=$server_part[0];
    $mixed["port"]=$server_part[1];
    $mixed["protocol"]=$server_part[2];
    $mixed["method"]=$server_part[3];
    $mixed["obfs"]=$server_part[4];
    $mixed["password"]=base64_decode($server_part[5]);
    parse_str($i[1],$param_part);
    if (array_key_exists("remarks",$param_part)){
        $mixed['name']=base64_decode($param_part['remarks']);
    }
    if (array_key_exists("obfsparam",$param_part)){
        $mixed['obfsparam']=base64_decode($param_part['obfsparam']);
    }
    if (array_key_exists("protoparam",$param_part)){
        $mixed['protoparam']=base64_decode($param_part['protoparam']);
    }
    if (array_key_exists("group",$param_part)){
        $mixed['group']=base64_decode($param_part['group']);
    }
    return $mixed;
}

function sql_ssr_add($mixed){
    global $con;
    $basic_string="`name`,`server`,`port`,`protocol`,`method`,`obfs`,`keys`";
    if (!array_key_exists("name",$mixed)){
        $mixed['name']="Other Unknown";
    }    
    $basic_var="'".$mixed['name']."','".$mixed['server']."','".$mixed['port']."','".$mixed['protocol']."','".$mixed['method']."','".$mixed['obfs']."','".$mixed['password']."'";
    if (array_key_exists("obfsparam",$mixed)){
        $basic_string.=",`obfsparam`";
        $basic_var.=",'".$mixed['obfsparam']."'";
    }
    if (array_key_exists("protoparam",$mixed)){
        $basic_string.=",`protoparam`";
        $basic_var.=",'".$mixed['protoparam']."'";
    }
    $sql="INSERT INTO `ssr` ($basic_string) VALUES ($basic_var);";
    mysql_query($sql,$con);
    return "OK";
}

function ss_link_parser($ss_link){
    $mixed=[];
    $ss_link=str_replace("-","+",$ss_link);
    $ss_link=str_replace("_","/",$ss_link);
    $_p = explode("://",$ss_link);
    $p=explode("@",$_p[1],2);
    if(count($p)==2){
        $infos=explode("#",$p[1],2);
        $mixed['name']=urldecode($infos[1]);
        $server_part = explode($infos[0]);
        $mixed["server"]=$server_part[0];
        $mixed["port"]=$server_part[1];
        $a=base64_decode($p[0]);
        $method_part=explode(":",$a);
        $mixed["method"]=$method_part[0];
        $mixed["password"]=$method_part[1];
    }else{
        $a=base64_decode($p[0]);
        $_p=explode("@",$a);
        $method_part=explode(":",$_p[0]);
        $mixed["method"]=$method_part[0];
        $mixed["password"]=$method_part[1];
        $server_part=explode(":",$_p[1]);
        $mixed["server"]=$server_part[0];
        $mixed["port"]=$server_part[1];
    }
    return $mixed;
}

function ss_link_builder($mixed){
    $server=$mixed["server"];
    $port=$mixed["port"];
    $method=$mixed["method"];
    $password=$mixed["password"];
    if ($server=="" || $port=="" || $method=="" || $password==""){
        return "";
    }
    if (array_key_exists("name",$mixed)){
        $name="#".urlencode($mixed["name"]);
    }
    $ss_link=$method.":".$password."@".$server.":".$port;
    $ss_link=str_replace("=","",base64_encode($ss_link));
    $ss_link=str_replace("+","-",$ss_link);
    $ss_link=str_replace("/","_",$ss_link);
    $ss_link="ss://".$ss_link.$name;
    return $ss_link;
}

?>
