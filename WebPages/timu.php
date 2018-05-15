<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>My Small Site</title>
</head>
<body>
<?php
$con = mysqli_connect("localhost","root","Bd960912");
if (!$con){
    die('Could not connect: ' . mysqli_error($con));
}
mysqli_select_db($con,"jerry");
function get_timu($sid,$Lei,$T_type,$count){
    global $con;
    $sid=(int)$sid;
    $Lei = str_replace("'","",str_replace("\"","",str_replace(";","",$Lei)));
    $q_sql="SELECT * FROM `medtiku`";
    $c_sql="SELECT COUNT(1) FROM `medtiku`";
    if ($sid!=0 || $Lei!=0 || ($T_type <= 4 && $T_type >= 1)){
        $q_sql=$q_sql." WHERE";
        $c_sql=$c_sql." WHERE";
        $need_AND=FALSE;
        if (!$sid==0){
            if ($need_AND){
                $q_sql=$q_sql." AND";
                $c_sql=$c_sql." AND"; 
            }
            $q_sql=$q_sql." `sid`=$sid";
            $c_sql=$c_sql." `sid`=$sid";
            $need_AND=True;            
        }
        if (!$Lei==0){
            if ($need_AND){
                $q_sql=$q_sql." AND";
                $c_sql=$c_sql." AND"; 
            }
            $q_sql=$q_sql." `Lei`='$Lei'";
            $c_sql=$c_sql." `Lei`='$Lei'";
            $need_AND=True;            
        }
        if (!$T_type==0){
            if ($need_AND){
                $q_sql=$q_sql." AND";
                $c_sql=$c_sql." AND"; 
            }
            $q_sql=$q_sql." `T_Type`=$T_type";
            $c_sql=$c_sql." `T_Type`=$T_type";
            $need_AND=True;            
        }
    }
    $row = mysqli_fetch_array(mysqli_query($con,$c_sql))[0];
    if ($count<=1){
        $is = [array_rand(range(1,$row),1)];
    }else{
        $is = array_rand(range(1,$row),$count);        
    }
    $res=[];
    foreach ( $is as $i ){
        $i=(String) $i;
        $sql=$q_sql." LIMIT $i,1";
        $tmpr=mysqli_query($con,$sql);
        $row = mysqli_fetch_assoc($tmpr);
        $res=array_merge($res,[$row]);
    } 
    return $res;
}
function get_biglei(){
    global $con;
    $sql="SELECT `BigLei` as 'name',`sid`,COUNT(1) as 'count' FROM medtiku GROUP BY `sid`";
    $tmpr=mysqli_query($con,$sql);
    $res=[];
    while($row = mysqli_fetch_assoc($tmpr)){
        $res=array_merge($res,[$row]);        
    }
    return $res;
}
function get_lei($sid){
    global $con;
    $sql="SELECT `BigLei` AS 'bname',`sid`,`Lei` as 'name',COUNT(1) as 'count' FROM medtiku WHERE `sid`=".(int) $sid." GROUP BY `Lei`";
    $tmpr=mysqli_query($con,$sql);
    $res=[];
    echo(mysqli_error($con));
    while($row = mysqli_fetch_assoc($tmpr)){
        $res=array_merge($res,[$row]);        
    }
    return $res;
}

function timu_title_render($timu){
    #//标头
    $type=["Unknown","单选题","多选题","名词解释","问答题"];
    if ($timu==null){
        echo "<h1><a href='?sid=".$_GET['sid']."&Lei=".$_GET['Lei']."'>返回</a></h1>";
    }else{
        echo "<div><h2><a href='?sid=".$timu['sid']."'>".$timu['BigLei']."-></a></h2>
        <h1><a href='?sid=".$timu['sid']."&Lei=".$timu['Lei']."'>".$timu['Lei']."</a></h1>
        <h4>".$type[(int) $timu['T_Type']]."</h4></div><hr/>";
    }
}
function timu_t1_render($timu){
    #//单选题
    echo "<div><h4>".$timu['Ti']."</h4>
    <h5>".$timu['S_A']."</h5>
    <h5>".$timu['S_B']."</h5>
    <h5>".$timu['S_C']."</h5>
    <h5>".$timu['S_D']."</h5>
    <h5>".$timu['S_E']."</h5>
    <h6>答案：".$timu['Answer']."</h6>
    <h6>解析：".$timu['Note']."</h6></div>";
    echo "<hr/>";
}
function timu_t2_render($timu){
    #//多选题
    echo "<div><h4>".$timu['Ti']."</h4>
    <h5>".$timu['S_A']."</h5>
    <h5>".$timu['S_B']."</h5>
    <h5>".$timu['S_C']."</h5>
    <h5>".$timu['S_D']."</h5>
    <h5>".$timu['S_E']."</h5>
    <h6>答案：".$timu['Answer']."</h6>
    <h6>解析：".$timu['Note']."</h6></div>";
    echo "<hr/>";
}
function timu_t3_render($timu){
    #//名解题
    echo "<div><h4>".$timu['Ti']."</h4>
    <h5>详解：".$timu['Note']."</h5></div>";
    echo "<hr/>";
}
function timu_t4_render($timu){
    #//简答题
    echo "<div><h4>".$timu['Ti']."</h4>
    <h5>详解：".$timu['Note']."</h5></div>";
    echo "<hr/>";
}
function timu_main_render($timus){
    foreach($timus as $timu){
        timu_title_render($timu);
        if ($timu["T_Type"]==1){
            timu_t1_render($timu);
        }elseif ($timu["T_Type"]==2){
            timu_t2_render($timu);
        }elseif ($timu["T_Type"]==3){
            timu_t3_render($timu);
        }elseif ($timu["T_Type"]==4){
            timu_t4_render($timu);
        }else{
            echo "<h1>没有了呢</h1>";
            break;
        }
    }
}
function leibie_render($leibies){
    if (array_key_exists("bname",$leibies[0])){
        echo "<div><h1><a href='?'><--".$leibies[0]['bname']."--></a></h1></div>";
        echo "<div><h3><a href='?sid=".(String) $_GET['sid']."&Lei=0'>随机</a></h3></div><hr/>";
    }else{
        echo "<div><h1><--大类目--></h1></div>";
        echo "<div><h3><a href='?r&count=1'>随机</a></h3></div><hr/>";
    }
    foreach($leibies as $leibie){
        if (array_key_exists("sid",$_GET)){
            $url="?sid=".$leibie['sid']."&Lei=".$leibie['name'];
        }else{
            $url="?sid=".$leibie['sid'];
        }
        echo "<div><h3><a href='$url'>".$leibie['name']."</a></h3>
        <h5>数量：".$leibie['count']."</h5>";
        echo "<hr/>";
    }
}
function type_render($sid,$lei){
    $type=["Unknown","单选题","多选题","名词解释","问答题"];
    echo "<div><h1><a href='?sid=".(String) $_GET['sid']."'><--".$lei."--></a></h1></div>";  
    echo "<div><h2>小类目</h2></div>";
    echo "<div><h3><a href='?sid=".(String) $sid."&Lei=$lei&type=0'>随机</a></h3></div><hr/>";
    for ($i=1; $i<=4; $i++){
        echo "<div><h3><a href='?sid=".(String) $sid."&Lei=".$lei."&type=".(String) $i."'>".$type[$i]."</a></h3></div>";
    }    
}
if (array_key_exists('sid',$_GET)){
    if (array_key_exists('Lei',$_GET)){
        if (array_key_exists('type',$_GET)){
            timu_main_render(get_timu((int) $_GET['sid'],$_GET['Lei'],(int) $_GET['type'],1));
        }else{
            type_render((int) $_GET['sid'],$_GET['Lei']);
        }
    }else{
        leibie_render(get_lei($_GET['sid']));
    }
}else{
    if (array_key_exists('r',$_GET)){
        if (array_key_exists('count',$_GET)){
            timu_main_render(get_timu(0,0,0,(int)$_GET['count']));
        }else{
            timu_main_render(get_timu(0,0,0,1));
        }
    }else{
        leibie_render(get_biglei());
    }
}
?>
</body>
</html>