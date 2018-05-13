<?php
/**
 * 字母+数字的验证码生成
 */
while(True){
//1.创建黑色画布
$image = imagecreatetruecolor(160, 60);
 
//2.为画布定义(背景)颜色
$bgcolor = imagecolorallocate($image, 255, 255, 255);
 
//3.填充颜色
imagefill($image, 0, 0, $bgcolor);
 
// 4.设置验证码内容
 
//4.1 定义验证码的内容
$content = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
 
//4.1 创建一个变量存储产生的验证码数据，便于用户提交核对
$captcha = "";
for ($i = 0; $i < 4; $i++) {
    // 字体大小
    $fontsize = mt_rand(12,18);
    // 字体颜色
    $fontcolor = imagecolorallocate($image, mt_rand(0, 120), mt_rand(0, 120), mt_rand(0, 120));
    // 设置字体内容
    $fontcontent = substr($content, mt_rand(0, strlen($content)), 1);
    $captcha .= $fontcontent;
    // 显示的坐标
    $x = ($i * 160 / 4) + mt_rand(5, 25);
    $y = mt_rand(5, 25);
    // 填充内容到画布中
    imagestring($image, $fontsize, $x, $y, $fontcontent, $fontcolor);
}
if(strlen($captcha)!=4){
    print(strlen($captcha."\n"));
    continue;
}else{
    echo($captcha."\n");
}
//4.3 设置背景干扰元素
for ($$i = 0; $i < 200; $i++) {
    $pointcolor = imagecolorallocate($image, mt_rand(50, 200), mt_rand(50, 200), mt_rand(50, 200));
    imagesetpixel($image, mt_rand(1, 159), mt_rand(1, 59), $pointcolor);
}
 
//4.4 设置干扰线
for ($i = 0; $i < 3; $i++) {
    $linecolor = imagecolorallocate($image, mt_rand(50, 200), mt_rand(50, 200), mt_rand(50, 200));
    imageline($image, mt_rand(1, 159), mt_rand(1, 59), mt_rand(1, 159), mt_rand(1, 59), $linecolor);
}
//6.输出图片到浏览器
imagepng($image,"captcha/".$captcha.".png");
//7.销毁图片
imagedestroy($image);
}
?>