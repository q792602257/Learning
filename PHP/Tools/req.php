<?php
function getHTML($url,$method="GET",$headers=Null,$data=Null,$cookie=Null){
	$urlarr=parse_url($url);
	$req="";
	if($method=="POST" || $method=="GET"){}
	else{
		return "Invaild Method";
	}
	if($headers){
		foreach($headers as $key => $val){
			$req.=$key.": ".$val."\r\n";
		}
	}
	else{
		$req.= "Accept-Encoding: deflate\r\n";
		$req.= "Connection: keep-alive\r\n";
		$req.= "Referer: ".$url."\r\n";
		$req.= "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0\r\n\r\n";
	}
	if($cookie){
		$req.= "Cookie: ";
		foreach($cookie as $key => $val){
			$req.= $key.":".$val."; ";
		}
		$req.="\r\n";
	}
	$post="";
	if($method=="POST"){
		if(is_array($data)){
			$post=http_build_query($data);
		}
		else{
			$post=$data;
		}
		$req.= "Content-type: application/x-www-form-urlencoded\r\n";
		$req.= "Content-length: ".strlen($post)."\r\n";
	}
	if($method=="GET"){
		if(is_array($data)){
			$url.="?".http_build_query($data);
		}
	}
	$option=array($urlarr["scheme"]=>array("url"=>$url,"method"=>$method,"header"=>$req,"content"=>$post));
	$context=stream_context_create($option);
	$stream = fopen($url,"rb",false,$context);
	$_Rheader=stream_get_meta_data($stream)["wrapper_data"];
	$Rheader=[];
	foreach($_Rheader as $_L){
		$_eH = explode(":",$_L,2);
		if (count($_eH)<2){
			continue;
		}else{
			$Rheader[$_eH[0]]=$_eH[1];
		}
	}
	$html=stream_get_contents($stream);
	return array("html"=>$html,"header"=>$Rheader);
}
if(isset($_GET["url"])){
	$url=$_GET["url"];
}
else{
	$url = "http://scrmtest.changan.com.cn/scrm-app-web/auth/pic/send";
}
$ret=getHTML($url,"GET",Null,["picKey"=>2]);
$header=$ret["header"];
$html=$ret["html"];
// foreach(explode("\n",$header) as $line){
// 	header($line);
// }
print_r($header);
print_r($html);
?>
