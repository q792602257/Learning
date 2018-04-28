<!DOCTYPE html>
<html lang="zh_CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Server Monitor</title>
</head>
<body>

<?php
function get_status(){
    $data=[];
    $m = new MongoClient();
    $db = $m->test;
    $res = $db->servers_cpu->aggregate([["\$group"=>["_id"=>"\$ip","cpus"=>["\$last"=>"\$cpus"],"cpu_percent"=>["\$last"=>"\$cpu_percent"],"time"=>["\$last"=>"\$time"]]],["\$sort"=>["time"=>-1]]],['cursor'=>['batchSize'=>10000]]);
    foreach($res['cursor']['firstBatch'] as $r){
        if(!array_key_exists($r['_id'],$data)){
            $data[$r['_id']]=[];
        }
        $data[$r['_id']]['cpu']=[];
        foreach($r as $key=>$val){
            $data[$r['_id']]['cpu'][$key]=$val;
        }
    }
    $res = $db->servers_mem->aggregate([["\$group"=>["_id"=>"\$ip","mem_total"=>["\$last"=>"\$mem_total"],"mem_avail"=>["\$last"=>"\$mem_avail"],"mem_free"=>["\$last"=>"\$mem_free"],"swap_total"=>["\$last"=>"\$swap_total"],"swap_avail"=>["\$last"=>"\$swap_avail"],"swap_free"=>["\$last"=>"\$swap_free"],"time"=>["\$last"=>"\$time"]]]],['cursor'=>['batchSize'=>10000]]);
    foreach($res['cursor']['firstBatch'] as $r){
        if(!array_key_exists($r['_id'],$data)){
            $data[$r['_id']]=[];
        }
        $data[$r['_id']]['mem']=[];
        foreach($r as $key=>$val){
            $data[$r['_id']]['mem'][$key]=$val;
        }
    }
    $res = $db->servers_io->aggregate([["\$group"=>["_id"=>"\$ip","io_r"=>["\$last"=>"\$io_r"],"io_w"=>["\$last"=>"\$io_w"],"io_rB"=>["\$last"=>"\$io_rB"],"io_wB"=>["\$last"=>"\$io_wB"],"time"=>["\$last"=>"\$time"]]]],['cursor'=>['batchSize'=>10000]]);
    foreach($res['cursor']['firstBatch'] as $r){
        if(!array_key_exists($r['_id'],$data)){
            $data[$r['_id']]=[];
        }
        $data[$r['_id']]['io']=[];
        foreach($r as $key=>$val){
            $data[$r['_id']]['io'][$key]=$val;
        }
    }
    foreach($data as $ip=>$pd){
        $data[$ip]['login']=[];
        $res = $db->servers_login->find(['ip'=>$ip])->sort(["time"=>-1])->limit(3);
        $i = 0;
        foreach($res as $r){
            foreach($r as $key=>$val){
                if($key=='_id'){
                    continue;
                }
                $data[$ip]['login'][$i][$key]=$val;
            }
            $i++;
        }
    }
    return $data;
}
$data=get_status();
foreach($data as $ip=>$pdata){
    echo("
<div>
    <h1>$ip</h1><hr/>
    <h2>CPU情况<small>（更新时间：".date('Y-m-d H:i', $pdata['cpu']['time'])."）</small></h2>
    <h4>cpu核心数：".$pdata['cpu']['cpus']."个</h4>
    <h4>cpu使用率：".$pdata['cpu']['cpu_percent']."%</h4>
    <h2>内存情况<small>（更新时间：".date('Y-m-d H:i', $pdata['mem']['time'])."）</small></h2>
    <h4>内存剩余：".round($pdata['mem']['mem_avail']*100/$pdata['mem']['mem_total'],2)."% @ (". (int) ($pdata['mem']['mem_total']/1024/1024) ."M)</h4>
    ");
    if($pdata['mem']['swap_total']>0){
    echo("
    <h4>虚拟内存剩余：".round($pdata['mem']['swap_avail']*100/$pdata['mem']['swap_total'],2)."% @ (". (int) ($pdata['mem']['swap_total']/1024/1024) ."M)</h4>
    ");
    }
    echo("<h2>最近登陆情况</h2>
    ");
    if(count($pdata['login'])>0){
        foreach($pdata['login'] as $l){
            echo("
    <h4>From ".$l['from_ip']." Login as ".$l['user']."(Start @ ".$l['start_time'].")</h4>
            ");
        }
    }else{
        echo("<h3>暂无</h3>");
    }
    echo("
    <hr/>
</div>");
}
?>
</body>
</html>