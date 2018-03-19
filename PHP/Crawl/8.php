<?php
function pLogin()//$id,$pass)//无法处理登录失败的情况，不要输错帐号了
{
    $curl = curl_init() or die('竟然没有cUrl模块，被你气死了……死了……了……');//用curl
    $lpost = array(//POST DATA
        'pixiv_id'=>'jerryyan0912',
        'pass'=>'YAN1HAO',
        'mode'=>'login',
        'skip'=>'1'
    );
    curl_setopt($curl, CURLOPT_URL, "https://www.pixiv.net/login.php");
    curl_setopt($curl, CURLOPT_POST, count($lpost));
    curl_setopt($curl, CURLOPT_POSTFIELDS, $lpost);
    curl_setopt($curl, CURLOPT_COOKIEJAR, '.cookie');//cookie文件，下载文件要用到
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($curl, CURLOPT_HEADER, 1);
    curl_setopt($curl, CURLOPT_NOBODY, false);
    curl_setopt($curl, CURLOPT_REFERER, 'https://www.pixiv.net/login.php?return_to=0');
    curl_setopt($curl, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0');
    curl_exec($curl);
    curl_close($curl);
    echo "登录部分处理完毕\n";
}
function getHtml($url,$ref)//获取网页数据
{
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_COOKIEJAR, '.cookie');
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($curl, CURLOPT_HEADER, 0);
    curl_setopt($curl, CURLOPT_NOBODY, false);
    curl_setopt($curl, CURLOPT_REFERER, 'https://www.pixiv.net/login.php?return_to=0');
    curl_setopt($curl, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0');
    $html = curl_exec($curl);
    return $html;
}
function fileWrite($data,$fileName)//写文件用的函数
{
    $ext='.jpg';
    if (!file_exists('Pimg/')){mkdir('Pimg/');}
    $imgf = fopen('Pimg/' . $fileName . $ext, 'wb') or die('竟无法操作  Pimg/' . $fileName . $ext . "  ，那只好被你气死咯\n");
    fwrite($imgf,$data);
    fclose($imgf);
//     db_add('Pimg/' . $fileName . $ext);//日常留接口
}
pLogin();
$jData = json_decode(getHtml('https://www.pixiv.net/ranking.php?mode=daily&p=1&format=json','https://www.pixiv.net/ranking.php?mode=daily'),True);
for ($i=0;$i<count($jData['contents']);$i++)
{
    $durl = str_ireplace('c/240x480/img-master','img-master',$jData['contents'][$i]['url']);//取得真实图片链接
    if(file_exists('Pimg/'.$jData['contents'][$i]['illust_id'].'.jpg')){print '图片已存在  '.$jData['contents'][$i]['illust_id'].".jpg\n";continue;}//判断文件是否存在，存在即跳过
    $img = getHtml($durl,"http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id=".$jData['contents'][$i]['illust_id']."&page=0");//下载图片
    fileWrite($img,$jData['contents'][$i]['illust_id']);//写图片
    print '已下载图片  '.$jData['contents'][$i]['illust_id'].".jpg\n";
}

?>
