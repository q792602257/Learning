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
    if ($flag!=1){
        $sql.=" isKey='$flag' AND ";
    }
    $sql.=" `isValid`=TRUE;";
    $result = mysql_query($sql,$con);
    while($row = mysql_fetch_array($result)){
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
    }
    if ($flag!=1){
        $ret="MAX=3\r\n".$ret;
    }elseif($max!=0){
        $ret="MAX=$max\r\n".$ret;        
    }
    return $ret;
}

function ssr_link_builder($mixed){
    $server=$mixed["server"];
    $port=$mixed["port"];
    $protocol=$mixed["protocol"];
    $method=$mixed["method"];
    $obfs=$mixed["obfs"];
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
?>