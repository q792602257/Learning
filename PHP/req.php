<?php
function getHTML($url,$method="GET",$headers=Null,$data=Null,$cookie=Null){
	$url_array = parse_url($url);
	$req = "";
	if($method=="POST"){
		$req.= "POST ".$url." HTTP/1.0\r\n";
	}
	elseif($method=="GET"){
		$req.= "GET ".$url." HTTP/1.0\r\n";
	}
	$req.= "HOST : ".$url_array['host']."\r\n";
	if($headers){
		foreach($headers as $key => $val){
			$req.=$key." : ".$val."\r\n";
		}
	}
	else{
		$req.= "Accept-Encoding: deflate\r\n";
		$req.= "Connection: keep-alive\r\n";
		$req.= "Referer: ".$url."\r\n";
		$req.= "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0\r\n\r\n";
	}
	if($cookie){
		for($i=0;$i<count($cookie);$i++){
			$req.= "Cookie: ".$cookie[$i]."\r\n";
		}
	}
	if($method=="POST"){
		if(is_array($data)){
			$post=http_build_query($data);
		}
		else{
			$post=$data;
		}
		$req.= "Content-type: application/x-www-form-urlencoded\r\n";
		$req.= "Content-length: ".strlen($post)."\r\n";
		$req.= "\r\n".$post."\r\n\r\n";
	}
	if($url_array["scheme"]=="http"){
		$stream = fsockopen('http://'.$url_array['host'],80,$errno,$errstr,30);
	}
	elseif($url_array["scheme"]=="https"){
		$stream = fsockopen('ssl://'.$url_array['host'],443,$errno,$errstr,30);
	}
	fputs($stream,$req);
	$Rheader="";
	$cookieA=array();
	while(($line=trim(fgets($stream)))!=""){
		$Rheader.=$line."\r\n";  
		if(strstr($line,"Set-Cookie:")){ 
			list($coo,$cookieLine)=explode(" ",$line);  
			$cookieA[] = $cookieLine;  
		}
	}
	$html="";
	while (!feof($stream)){
		$html .= fgets($stream);  
	}
	return array("html"=>$html,"header"=>$Rheader);
}
if($_GET["url"]){
	$url=$_GET["url"];
}
else{
	$url = "https://jerry.jerryyan.top/";
}
$ret=getHTML($url);
$header=$ret["header"];
$html=$ret["html"];
// foreach(explode("\n",$header) as $line){
// 	header($line);
// }
print($html);
?>
