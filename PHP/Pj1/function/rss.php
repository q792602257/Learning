<?php
function build_html($title,$content,$url){
    echo('<div class="message"><div class="title">');
    echo($title);
    echo('</div><span class="content">');
    echo($content);
    echo('</span><div class="qrcode" data="');
    echo($url);
    echo('"></div></div>');
}
function get_and_parse_rss($url){
    @require_once('rss/rss_fetch.inc');
    $rss=@fetch_rss($url);
    foreach($rss->items as $item){
        build_html($item['title'],$item['summary'],$item['link']);
    }
}
echo('<div class="weatherInfo">这是刚刚更新的订阅</div>');
get_and_parse_rss('http://rss.sina.com.cn/news/china/focus15.xml');
get_and_parse_rss('http://news.qq.com/newsgn/rss_newsgn.xml');
get_and_parse_rss('http://rss.sina.com.cn/news/society/focus15.xml');
?> 