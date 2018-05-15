<?php
function emgjhkLogin($user,$pass){
	$login_url = "http://www.emgjhk.com/loginhome_new.php?action=login";
	$referer = "http://www.emgjhk.com/Template/login/20/index.php";
	$url_array = parse_url($login_url);
	$req = "";
	// $req.= "POST ".$url." HTTP/1.1\r\n";
	// $req.= "HOST: ".$url_array['host']."\r\n";
	$req.= "Connection: keep-alive\r\n";
	$req.= "Accept-Encoding: deflate\r\n";
	$req.= "Referer: ".$referer."\r\n";
	$req.= "Origin: http://www.emgjhk.com\r\n";
	$req.= "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0\r\n";
	if(isset($_COOKIE["PHPSESSID"])){
		$session=$_COOKIE["PHPSESSID"];
		$req.= "Cookie: PHPSESSID=".$session."\r\n";
	}
	$req.= "Content-Type: multipart/form-data; boundary=----WebKitFormBoundary0UBgeAJI3AhGpuxR\r\n";
	$post="";
	$post.="------WebKitFormBoundary0UBgeAJI3AhGpuxR\r\n";
	$post.="Content-Disposition: form-data; name=\"username\"\r\n\r\n".$user."\r\n";
	$post.="------WebKitFormBoundary0UBgeAJI3AhGpuxR\r\n";
	$post.="Content-Disposition: form-data; name=\"password\"\r\n\r\n".$pass."\r\n";
	$post.="------WebKitFormBoundary0UBgeAJI3AhGpuxR\r\n";
	$post.="Content-Disposition: form-data; name=\"remember\"\r\n\r\n1\r\n";
	$req.= "Content-length: ".strlen($post)."\r\n";
	// $req.= "\r\n".$post."\r\n";
	$options=array("http"=>array("url"=>$login_url,"method"=>"POST","header"=>$req,"content"=>$post));
	$context=stream_context_create($options);
	$stream = file_get_contents($login_url,false,$context);
	// $Rheader="";
	// while(($line=trim(fgets($stream)))!=""){
	// 	$Rheader.=$line."\r\n";  
	// 	if(strstr($line,"Set-Cookie:")){ 
	// 		list($coo,$cookieLine)=explode(" ",$line);  
	// 		$cookieA[] = $cookieLine;  
	// 	}
	// }
	// $html="";
	// while (!feof($stream)){
	// 	$html .= fgets($stream);  
	// }
	var_dump($stream);
	// var_dump($Rheader);
}
emgjhkLogin("123","234");
?>
