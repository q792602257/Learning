<?php
function getHtml($url){
    $options = [
        'http' => [
            'method' => 'GET',
            'timeout' => 30 // 超时时间（单位:s）
        ]
    ];
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    return $result;
}
$url="http://weatherapi.market.xiaomi.com/wtr-v3/weather/all?latitude=31.383602&longitude=121.502899&isLocated=true&locationKey=weathercn:101020300&days=15&appKey=weather20151024&sign=zUFJoAR2ZVrDy1vF3D07&romVersion=7.11.9&appVersion=102&alpha=false&isGlobal=false&device=ido&modDevice=ido_xhdpi&locale=zh_cn";
echo(getHtml($url));
?>