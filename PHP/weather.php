<?php
/*建议做成ajax动态加载
 *不会写前端的怨念
 */
function getHTML($url)
{
	$html = file_get_contents($url);
	return $html;
}
function getIP()
{
	static $realip;
	if (isset($_SERVER)) {
		if (isset($_SERVER["HTTP_X_FORWARDED_FOR"])) {
			$realip = $_SERVER["HTTP_X_FORWARDED_FOR"];
		}
		else if (isset($_SERVER["HTTP_CLIENT_IP"])) {
			$realip = $_SERVER["HTTP_CLIENT_IP"];
		}
		else {
			$realip = $_SERVER["REMOTE_ADDR"];
		}
	}
	else {
		if (getenv("HTTP_X_FORWARDED_FOR")) {
			$realip = getenv("HTTP_X_FORWARDED_FOR");
		}
		else if (getenv("HTTP_CLIENT_IP")) {
			$realip = getenv("HTTP_CLIENT_IP");
		}
		else {
			$realip = getenv("REMOTE_ADDR");
		}
	}
	return $realip;
}
function getLocation($ip = None)
{
	$url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json";
	if ($ip && preg_match("/(\d{1,3}\.){3}(\d{1,3})/",$ip)) {
		$url .="&ip=".$ip;
	}
	$ip = json_decode(file_get_contents($url), true);
	$data = $ip;

	return $data;
}
function city2code($city)
{
	// print($city);
	$html = getHTML("http://toy1.weather.com.cn/search?cityname=" . urlencode($city));
	preg_match("/\((.*)\)/", $html, $json);
	$jdata = json_decode($json[1],true);
	$code = explode("~",$jdata[0]["ref"])[0];
	return $code;
}
print_r(getLocation("64.137.206.200"));die();
if (isset($_SERVER)) {
	$city = getLocation(getIP());
}
else {
	$city = getLocation();
}
function weather($code){
	$html=getHTML("http://aider.meizu.com/app/weather/listWeather?cityIds=".$code);//魅族api，信息全
	// preg_match("/({.*})/", $html, $json);
	$jdata = json_decode($html,true);//输出jdata可以看到很多信息，自己猜是什么。。。贼全，建议做成ajax动态加载
	$city=$jdata["value"][0]["city"];
	$now=$jdata["value"][0]["realtime"];
	print($city."<br/>天气：".$now["weather"]."<br/>温度：".$now["temp"]."<br/>风力：".$now["wD"].$now["wS"]);
}
weather(city2code($city["city"]));
?>