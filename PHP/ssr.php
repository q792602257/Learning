<?php

include("SSR_Link.php");
$ret="";
if (array_key_exists("key",$_GET)){
    if ($_GET["key"]=="neyacat" || $_GET["key"]=="jerryyan"){
        if (array_key_exists("max",$_GET)){
            $max=(int)$_GET['max'];
        }else{
            $max=0;
        }
        $ret.=sql_ssr_get(1,$_GET["key"],$max);
    }else{
        $ret.=sql_ssr_get(0,"Jerry's SSR Group",3);
    }
    echo str_replace("=","",base64_encode($ret));
}elseif (array_key_exists("new",$_GET)) {
    echo(sql_ssr_add(ssr_link_parser($_GET["new"])));
}else{
    $ret.=sql_ssr_get(2,"NeyaCat's SSR Subscribe",3);
    echo str_replace("=","",base64_encode($ret));
}


?>