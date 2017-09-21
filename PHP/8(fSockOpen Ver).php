<?php
function pLogin()//$id,$pass)//无法处理登录失败的情况，不要输错帐号了
{
    $rheader = '';
    $request  = "POST https://www.pixiv.net/login.php HTTP/1.0\r\n";
    $request .= "Host : www.pixiv.net\r\n";
    $request .= "Accept-Encoding: deflate\r\n";
    $request .= "Connection: keep-alive\r\n";
    $request .= "Referer: https://www.pixiv.net/login.php?return_to=0\r\n";
    $request .= "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0\r\n";
    $lpost = http_build_query(array(//POST DATA
        'pixiv_id'=>'jerryyan0912',
        'pass'=>'YAN1HAO',
        'mode'=>'login',
        'skip'=>'1'
    ));
    $request .= "Content-type: application/x-www-form-urlencoded\r\n";
    $request .= 'Content-length: '.strlen($lpost)."\r\n";
    $request .= "\r\n".$lpost."\r\n\r\n";
    $conn = fsockopen('ssl://www.pixiv.net',443,$errno,$errstr,60);
    fputs($conn,$request);
    $cookieStr=array();
    while(($line=trim(fgets($conn)))!="")     
    {
        $rheader.=$line;  
        if(strstr($line,"Set-Cookie:"))     
        {     
            list($coo,$cookieLine)=explode(" ",$line);  
            $cookieStr[] = $cookieLine;  
        }   
    }
    echo "登录部分处理完毕\n";
    return $cookieStr;
}
function getHtml($url,$cookie,$ref)//获取网页数据
{
    $rheader = '';
    $html = '';
    $url_array = parse_url($url);
    $request  = "GET ".$url." HTTP/1.0\r\n";
    $request .= "Host : ".$url_array['host']."\r\n";
    $request .= "Accept-Encoding: deflate\r\n";
    $request .= "Connection: keep-alive\r\n";
    $request .= "Referer: ".$ref."\r\n";
    for($i=0;$i<count($cookie);$i++)
    {
        $request .= "Cookie: ".$cookie[$i]."\r\n";
    }
    $request .= "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0\r\n\r\n";
    $conn = fsockopen('ssl://'.$url_array['host'],443,$errno,$errstr,60);
    fwrite($conn,$request);
    while( ($line=trim(fgets($conn))) != "" )
    {
        $rheader.=$line;
    }
    while (!feof($conn)) 
    {  
        $html .= fread($conn,32768);  
    }
    return $html;
}
function fileWrite($URL,$fileName,$cookie)//写文件用的函数
{
    $dir='Pimg/';
    $ext='.jpg';
    if(!file_exists($dir)){mkdir($dir,0777,True);}//建文件夹
    if(file_exists($dir.$fileName.$ext)){print '图片已存在  '.$fileName.$ext."\n";return;}//判定文件是否存在，存在就退出函数
    $data = getHtml($URL,$cookie,"http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id=".$fileName."&page=0");//下载图片
    $imgf = fopen($dir.$fileName.$ext,'wb') or die('竟无法操作  '.$dir . $fileName . $ext . "  ，那只好被你气死咯\n");
    fwrite($imgf,$data);
    fclose($imgf);
    print '已下载图片  '.$dir.$fileName.".jpg\n";
//     db_add('Pimg/' . $fileName . $ext);//日常留接口
}
$cookie = pLogin();
$jData = json_decode(getHtml('https://www.pixiv.net/ranking.php?mode=daily&p=1&format=json',$cookie,'https://www.pixiv.net/ranking.php?mode=daily'),True);
for ($i=0;$i<count($jData['contents']);$i++)
{
    fileWrite(str_ireplace('c/240x480/img-master','img-master',$jData['contents'][$i]['url']),$jData['contents'][$i]['illust_id'],$cookie);//下载并写图片
}

?>
