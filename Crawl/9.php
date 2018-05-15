<?php
function pLogin()//$id,$pass)//无法处理登录失败的情况，不要输错帐号了
{	
	$curl = curl_init() or die('竟然没有cUrl模块，被你气死了……死了……了……');//用curl
    $header=array(
            'App-OS'=>'ios',
            'App-OS-Version'=>'10.3.1',
            'App-Version'=>'6.7.1',
            'User-Agent'=>'PixivIOSApp/6.7.1 (iOS 10.3.1; iPhone8,1)',
    );
	$lpost = array(
            'get_secure_url'=> 1,
            'client_id'=>'bYGKuGVw91e0NMfPGp44euvGt59s',
            'client_secret'=>'HP3RmkgAmEGro0gn1x9ioawQE8WMfvLXDz3ZqxpK',
            'grant_type'=>"password",
            "username"=>"1193031227",
            "password"=>"CC1123yhq",
    );
	curl_setopt($curl, CURLOPT_URL, "https://oauth.secure.pixiv.net/auth/token");
	curl_setopt($curl, CURLOPT_POST, count($lpost));
	curl_setopt($curl, CURLOPT_POSTFIELDS, $lpost);
// 	curl_setopt($curl, CURLOPT_COOKIEJAR, '.cookie');//cookie文件，下载文件要用到
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($curl, CURLOPT_HEADER, 0);
	curl_setopt($curl, CURLOPT_HTTPHEADER, $header);
	curl_setopt($curl, CURLOPT_NOBODY, false);
// 	curl_setopt($curl, CURLOPT_REFERER, 'https://www.pixiv.net/login.php?return_to=0');
	curl_setopt($curl, CURLOPT_USERAGENT, 'PixivIOSApp/6.7.1 (iOS 10.3.1; iPhone8,1)');
	$html=curl_exec($curl);
	curl_close($curl);
	echo "登录部分处理完毕<br>\n";
	print $html;
	/*print_r(*/
	return json_decode($html,true);
	/*);die*/;
}
function getHtml(/*$url,$ref,*/$token)//获取网页数据
{
	$curl = curl_init();
    $header=array(
            'App-OS'=>'ios',
            'App-OS-Version'=>'10.3.1',
            'App-Version'=>'6.7.1',
//             "Authorization"=>"Bearer {$token}",
            'User-Agent'=>'PixivIOSApp/6.7.1 (iOS 10.3.1; iPhone8,1)',
    );
//     print "\n{$token}\n";
    $g=http_build_query(array(
//             'word'=>"cirno",
//             'search_target'=>"partial_match_for_tags",
//             'sort'=>"date_desc",
//                 'user_id'=>"26061036",
//                 'filter'=>'for_ios',
            'access_token'=> $token,
            'mode'=>"daily",
            'page'=>"1",
            'per_page'=>"50",
            'include_stats'=>1,
            'include_sanity_level'=>1,
            'image_sizes'=>'large',
            'profile_image_sizes'=>'px_170x170',
        ));
    $url="https://public-api.secure.pixiv.net/v1/ranking/all.json";
    print "\n{$url}?{$g}\n";
	curl_setopt($curl, CURLOPT_URL, $url."?".$g);
// 	curl_setopt($curl, CURLOPT_COOKIEJAR, '.cookie');
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($curl, CURLOPT_HTTPHEADER, $header);
	curl_setopt($curl, CURLOPT_HEADER, 0);
	curl_setopt($curl, CURLOPT_NOBODY, false);
// 	curl_setopt($curl, CURLOPT_REFERER, "http://spapi.pixiv.net" );
	curl_setopt($curl, CURLOPT_USERAGENT, 'PixivIOSApp/6.7.1 (iOS 10.3.1; iPhone8,1)');
	$html = curl_exec($curl);
	print_r(json_decode($html));die;
	return $html;
}
function bang($No,$pages=1)
{
	if($No > 7 or $No < 0){die;}
	$bangs=array(
	array("日","daily"),
	array("周","weekly"),
	array("月","monthly"),
	array("Rookie","rookie"),
	array("Original","original"),
	array("B","femal"),
	array("G","male"),
	);
	print "你选择的是{$bangs[$No][0]}榜<br>\n";
	for($ss=1;$ss<=$pages;$ss++){
		print "正在获取榜单目录<br>";
		$jData = json_decode(getHtml("https://www.pixiv.net/ranking.php?mode={$bangs[$No][1]}&p={$ss}&format=json","https://www.pixiv.net/ranking.php?mode={$bangs[$No][1]}"),True);
		print "获取成功，共有".count($jData['contents'])."条数据<br>\n";
		for ($i=0;$i<count($jData['contents']);$i++)
		{
			$durl = str_ireplace('c/240x480/img-master','img-master',$jData['contents'][$i]['url']);//取得真实图片链接
			print "处理第 ".($i+1)." 条数据中……<br>\t";
			fileWrite($durl,$jData['contents'][$i]['illust_id']);
		}
	}
}
function sousuo($string,$pages=1)
{
	print "搜索关键词为：\t{$string}<br>\n";
	for($ss=1;$ss<=$pages;$ss++){
		print "正在获取第{$ss}页的搜索结果<br>\t";
		$html = getHtml("https://www.pixiv.net/search.php?word={$string}&s_mode=s_tag_full&order=date_d&p={$ss}","https://www.pixiv.net/search.php?s_mode=s_tag_full&word={$string}");/*html页面，用正则*/
		preg_match_all('/\&amp\;p=(\d+?)" rel="next" class="_button" title="次へ"/',$html,$isNext);
		preg_match_all('/"thumbnail-filter lazy-image"data-src="(.+?)"/',$html,$durl);
		print "获取成功，共有".count($durl[1])."条数据<br>\n";
		for ($i=0;$i<count($durl[1]);$i++)
		{
			preg_match('/(\d+?)_p0/',$durl[1][$i],$id);
			$url = str_ireplace('c/150x150/img-master','img-master',$durl[1][$i]);//取得真实图片链接
			print "处理第 ".($i+1)." 条数据中……<br>\t";
			fileWrite($url,$id[1]);//写图片
		}
		if(count($isNext[1])==0){print "<b>没有下一页了<b><br>\n" ;break;}else{print "继续爬取下一页页数据<br>\n";}
	}
}
function fileWrite($URL,$fileName)//下载图片用的函数
{
	$dir='Pixiv_images/P_sousuo/'.$_POST['name'].'/';
	$ext='.png';
	if(!file_exists($dir)){mkdir($dir,0777,True);}//建文件夹
	if(file_exists($dir.$fileName.$ext)){print '图片  '.$fileName.$ext."  已存在<br>\n";return;}//判定文件是否存在，存在就退出函数
	$data = getHtml($URL,"http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id=".$fileName."&page=0");//下载图片
	$imgf = fopen($dir.$fileName.$ext,'wb') or die('竟无法操作  '.$dir . $fileName . $ext . "  ，那只好被你气死咯<br>\n");
	fwrite($imgf,$data);
	fclose($imgf);
	print '已下载图片  '.$dir.$fileName.$ext."<br>\n";
//	db_add('Pimg/' . $fileName . $ext);//日常留接口
}

getHtml(pLogin()['response']['refresh_token']);
// $_POST['name'] = "東方project";
// sousuo("東方project",100);

?>
