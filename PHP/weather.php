<?php
/*建议做成ajax动态加载
 *不会写前端的怨念
 */
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
function getLocationComp($ip = None)
{
	$url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json";
	if ($ip && preg_match("/(\d{1,3}\.){3}(\d{1,3})/", $ip)) {
		$url .= "&ip=" . $ip;
	}
	$ip = json_decode(file_get_contents($url), true);
	$data = $ip;

	return $data;
}
function getLocation($ip = None)
{
	$url = "http://api.map.baidu.com/location/ip?ak=dfmB0CiyVLwaDWAI8sG0SSyHMjHU4RIS";
	if ($ip && preg_match("/(\d{1,3}\.){3}(\d{1,3})/", $ip)) {
		$url .= "&ip={$ip}";
	}
	$content = file_get_contents($url);
	$json = json_decode($content,TRUE);
	return $json;//->{'content'}->{'address'};//按层级关系提取address数据&coor=bd09ll

}
function city2code($city)
{
	if(strpos($city,"市")){
		$city = substr($city,0,strpos($city,"市"));
	}
	$html = file_get_contents("http://toy1.weather.com.cn/search?cityname=" . urlencode($city));
	preg_match("/\((.*)\)/", $html, $json);
	$jdata = json_decode($json[1], true);
	$code = explode("~", $jdata[0]["ref"])[0];
	return $code;
}
function weather($code)
{
	$html = file_get_contents("http://aider.meizu.com/app/weather/listWeather?cityIds=" . $code);//魅族api，信息全
	// preg_match("/({.*})/", $html, $json);
	$jdata = json_decode($html, true);//输出jdata可以看到很多信息，自己猜是什么。。。贼全，建议做成ajax动态加载
	$city = $jdata["value"][0]["city"];
	$now = $jdata["value"][0]["realtime"];
	print ($city . "<br/>天气：" . $now["weather"] . "<br/>温度：" . $now["temp"] . "<br/>风力：" . $now["wD"] . $now["wS"]);
}
if (isset($_SERVER)) {
	$city = getLocation(getIP());
}
else {
	$city = getLocation();
}
weather(city2code($city["content"]["address_detail"]["city"]));
?>