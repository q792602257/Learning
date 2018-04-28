<?php

function write_data($s,$ip){
    $m = new MongoClient();
    $db = $m->test;
    $data = json_decode($s,True);
    if(array_key_exists('cpu',$data)){
        $cpus=$data['cpu']['count'];
        $cpu_percent=array_sum($data['cpu']['percent'])/count($data['cpu']['percent']);
        $db->servers_cpu->insert([
            'ip'=>$ip,
            'cpus'=>$cpus,
            'cpu_percent'=>$cpu_percent,
            'time'=>time(),
        ]);
    };
    if(array_key_exists('mem',$data)){
        $mem_total=$data['mem']['total'];
        $mem_avail=$data['mem']['avail'];
        $mem_free=$data['mem']['free'];
        $swap_total=$data['mem']['swap']['total'];
        $swap_avail=$data['mem']['swap']['free'];
        $swap_free=$data['mem']['swap']['free'];
        $db->servers_mem->insert([
            'ip'=>$ip,
            'mem_total'=>$mem_total,
            'mem_avail'=>$mem_avail,
            'mem_free'=>$mem_free,
            'swap_total'=>$swap_total,
            'swap_avail'=>$swap_avail,
            'swap_free'=>$swap_free,
            'time'=>time(),
        ]);
    }
    if(array_key_exists('disk',$data)){
        $io_r=$data['disk']['io']['r'];
        $io_w=$data['disk']['io']['w'];
        $io_rB=$data['disk']['io']['rB'];
        $io_wB=$data['disk']['io']['wB'];
        $db->servers_io->insert([
            'ip'=>$ip,
            'io_r'=>$io_r,
            'io_w'=>$io_w,
            'io_rB'=>$io_rB,
            'io_wB'=>$io_wB,
            'time'=>time(),
        ]);
    }
    if(array_key_exists('login',$data)){
        foreach($data['login'] as $login){
            $user=$login['user'];
            $ts=$login['start'];
            $from_ip=$login['ip'];
            if($db->servers_login->find([
                'ip'=>$ip,
                'start_time'=>$ts,
            ])->count() > 0){

            }else{
                $db->servers_login->insert([
                    'ip'=>$ip,
                    'user'=>$user,
                    'from_ip'=>$from_ip,
                    'start_time'=>$ts,
                    'time'=>time(),
                ]);
            }
        }
    }
}
$postStr = file_get_contents("php://input");
print($_SERVER['REMOTE_ADDR']);
print("</br>\n");
$f = fopen('log','a');
fwrite($f,$_SERVER['REMOTE_ADDR']);
fwrite($f,"--------------------\r\n");
fwrite($f,$postStr);
fwrite($f,"\r\n\r\n");
write_data($postStr,$_SERVER['REMOTE_ADDR']);
?>