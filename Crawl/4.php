<?php
function getHtml($url)//获取网页数据
{
    $html = file_get_contents($url,False,stream_context_create(array('http'=>array('method'=>"GET",'timeout'=>5,))));//超时设置
    if($html){return $html;}
    else{print 'Retry';getHtml($url);}//这里有输出，如果请求太长就重试，大佬改一下重试几次就死了我们看吧
}
function fileWrite($data,$fileName,$ext)//写文件用的函数--未使用
{
    if (!file_exists('wall1/')){mkdir('wall1/');}
    $imgf = fopen('wall1/' . $fileName . $ext, 'w') or die('好气啊，竟然无法操作  wall1/' . $fileName . $ext . '  ，那只好死给你看咯');
    fwrite($imgf,$data);
    fclose($imgf);
    db_add('wall1/' . $fileName . $ext);
//     if (!isHRLS('wall1/'.$fileName.$ext)[0]){unlink('wall1/'.$fileName.$ext);}
}
function db_add($fn)
{
    //数据库连接和添加函数，大佬写一下吧我没数据库试（偷懒脸）
    //数据库随机取一条的代码是 FROM `表名` AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM `表名`)-(SELECT MIN(id) FROM `表名`))+(SELECT MIN(id) FROM `表名`)) AS id) AS t2 WHERE t1.id >= t2.id ORDER BY t1.id LIMIT 1;  
}
function isHRLS($url)//高分辨率判定&横纵判定T:横;F:纵---这个站全是1080p的壁纸，不用判断
{
    $temp=getimagesize($url);
    if ($temp[0]>800 and $temp[1]>600)
    {
        $HR = True;
    }
    else
    {
        $HR = False;
    }
    if ($temp[0]>$temp[1])
    {
        $LS = True;
    }
    else
    {
        $LS = False;
    }
    return array($HR,$LS);
}
function fetchImg($turl)//主做下载图片用
{
    $IDs = [];
    $urls = array();
    $dID = array();
    $thtml = getHtml($turl );//网页url,返回网页数据
    preg_match_all('/\<li\>\<a href\=\"\/desk\/(\d+?)\.htm/',$thtml,$ID);//解析id为获取真实链接做准备
    $IDs = array_merge_recursive($IDs,$ID[1]);//整合图片ID
    for ($n = 0 ; $n < count($IDs) ; $n++) //（获取图片url，可rand可爬）--rand()版
    {
        $i = intval(rand(0,count($IDs)-1));
        $url='http://www.netbian.com/desk/' . $IDs[$i] . '-1920x1080.htm';
        $html = getHtml($url);
        preg_match('/\<td align="left"\>\n\<img src="(.+?)"/',$html,$durl);//解析下载页面,匹配链接
        if (count($durl[1])==0){print $url;continue;}//誓死不开VIP
    //     print $durl[1] . "\n";die;//壁纸链接
        array_push($urls,$durl[1]);//$url[1]是图片真实链接,不需要下载要把后面下载功能注释了
        array_push($dID,$IDs[$i]);//获取序号，命名用
    }
    for ($j = 0 ; $j < count($urls) ; $j++)//下载图片
    {
        preg_match('/(\.(\w+)\?)|(\.(\w+)$)/',$urls[$j],$ext);//正则匹配一下后缀
        $pic = getHtml($urls[$j]);//获取图片
        fileWrite($pic,$dID[$j],$ext[0]);//写文件
    }
}
$urlb="http://www.netbian.com/";
$LB = array("fengjing","jianzhu",'huahui',"sheji");
foreach ($LB as $i)//也就爬个4个类别再说（滑稽（网速好出结果快）大概5,60张图吧
{
    fetchImg($urlb.$i);
    for($n=2;$n<10;$n++)//第二页以后的网址，爬个10页差不多了
    {
        fetchImg($urlb.$i.'/index_'.$n.'.htm');
    }
}
?>
