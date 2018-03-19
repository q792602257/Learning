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
	$option=array($urlarr["scheme"]=>array("url"=>$url,"method"=>$method,"header"=>$req,"content"=>$post));
	$context=stream_context_create($option);
	$stream = fopen($url,"r",false,$context);
	$Rheader=stream_get_meta_data($stream)["wrapper_data"];
	$html=stream_get_contents($stream);
	return array("html"=>$html,"header"=>$Rheader);
}
if(isset($_GET["url"])){
	$url=$_GET["url"];
}
else{
	$url = "https://www.himei.top/";
}
$ret=getHTML($url);
$header=$ret["header"];
$html=$ret["html"];
// foreach(explode("\n",$header) as $line){
// 	header($line);
// }
print_r($header);
?>
