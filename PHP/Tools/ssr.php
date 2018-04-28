<?php

include("SSR_Link.php");
$ret="";
echo str_replace("=","",base64_encode($ret));
if (array_key_exists("new",$_GET)) {
    echo(sql_ssr_add(ssr_link_parser($_GET["new"])));
}elseif (array_key_exists("ss",$_GET)){
    var_dump(ss_link_parser($_GET['ss']));
}elseif (array_key_exists("ssr",$_GET)){
    var_dump(ssr_link_parser($_GET['ssr']));
}else{
    $ret.=sql_ssr_get(2,"NeyaCat's SSR Subscribe",3);
    echo str_replace("=","",base64_encode($ret));
}

?>
