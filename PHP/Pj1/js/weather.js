var city = "宝山";
var weathercode={
    //|| Normal||DayTime|| Night ||
    0:["\uf00d","\uf00d","\uf02e"],//"晴",
    1:["\uf013","\uf002","\uf086"],//"多云",
    2:["\uf041","\uf041","\uf041"],//"阴",
    3:["\uf00b","\uf00b","\uf02b"],//"阵雨",
    4:["\uf016","\uf005","\uf025"],//"雷阵雨",
    5:["\uf01e","\uf068","\uf069"],//"雷阵雨并伴有冰雹",
    6:["\uf0b5","\uf0b2","\uf0b4"],//"雨夹雪",
    7:["\uf01c","\uf01c","\uf01c"],//"小雨",
    8:["\uf01a","\uf009","\uf029"],//"中雨",
    9:["\uf019","\uf008","\uf028"],//"大雨",
    10:["\uf018","\uf007","\uf027"],//"暴雨",
    11:["\uf017","\uf006","\uf026"],//"大暴雨",
    12:["\uf017","\uf006","\uf026"],//"特大暴雨",
    13:["\uf01b","\uf00a","\uf02a"],//"阵雪",
    14:["\uf01b","\uf00a","\uf02a"],//"小雪",
    15:["\uf01b","\uf00a","\uf02a"],//"中雪",
    16:["\uf01b","\uf065","\uf02a"],//"大雪",
    17:["\uf064","\uf065","\uf067"],//"暴雪",
    18:["\uf014","\uf003","\uf04a"],//"雾",
    19:["\uf076","\uf076","\uf076"],//"冻雨",
    20:["\uf082","\uf082","\uf082"],//"沙尘暴",
    21:["\uf01c","\uf00b","\uf02b"],//"小雨-中雨",
    22:["\uf01a","\uf009","\uf029"],//"中雨-大雨",
    23:["\uf019","\uf008","\uf028"],//"大雨-暴雨",
    24:["\uf017","\uf006","\uf026"],//"暴雨-大暴雨",
    25:["\uf017","\uf006","\uf026"],//"大暴雨-特大暴雨",
    26:["\uf01b","\uf00a","\uf02a"],//"小雪-中雪",
    27:["\uf01b","\uf00a","\uf02a"],//"中雪-大雪",
    28:["\uf01b","\uf00a","\uf02a"],//"大雪-暴雪",
    29:["\uf082","\uf082","\uf082"],//"浮沉",
    30:["\uf082","\uf082","\uf082"],//"扬沙",
    31:["\uf082","\uf082","\uf082"],//"强沙尘暴",
    32:["\uf050","\uf050","\uf050"],//"飑",
    33:["\uf056","\uf056","\uf056"],//"龙卷风",
    34:["\uf064","\uf065","\uf067"],//"若高吹雪",qnmd
    35:["\uf014","\uf003","\uf04a"],//"轻雾",
    53:["\uf074","\uf074","\uf074"],//"霾",
    99:["\uf07b","\uf07b","\uf07b"]//"未知"
};
var wind_level=["\uf0b7","\uf0b8","\uf0b9","\uf0ba","\uf0bb","\uf0bc","\uf0bd","\uf0be","\uf0bf","\uf0c0","\uf0c1","\uf0c2","\uf0c3"];
function parse_wind_level(spd){
    spd = parseFloat(spd);
    if (spd > 0 && spd < 1) {
        return 0;
    }else if (spd < 6){
        return 1;
    }else if (spd < 11){
        return 2;
    }else if (spd < 19){
        return 3;
    }else if (spd < 28){
        return 4;
    }else if (spd < 38){
        return 5;
    }else if (spd < 49){
        return 6;
    }else if (spd < 61){
        return 7;
    }else if (spd < 74){
        return 8;
    }else if (spd < 88){
        return 9;
    }else if (spd < 102){
        return 10;
    }else{
        return 11;
    }
}
function dataLeftCompleting(bits, identifier, value){
    value = Array(bits + 1).join(identifier) + value;
    return value.slice(-bits);
}
function compare(a,b){
    if (a>b){
        return "gt";
    }else if (a<b){
        return "lt";
    }else{
        return "eq";
    }
}
function build_time(date){
    var ret = "";
    var time = new Date();
    if(date.getDate()-time.getDate()  == 1){
        ret+= "明天";
    }else if(date.getDate()-time.getDate()  == 2){
        ret+= "后天";
    }else if(date.getDate()-time.getDate()  > 2){
        ret+= (date.getDate()-time.getDate()).toString() + "天后"
    }else if(date.getDate()-time.getDate()  == -1){
        ret+= "昨天";
    }else if(date.getDate()-time.getDate()  == -2){
        ret+= "前天";
    }else if(date.getDate()-time.getDate()  < -2){
        ret+= (date.getDate()-time.getDate()).toString() + "天前"
    }
    ret+=dataLeftCompleting(2, "0", date.getHours())+":"+dataLeftCompleting(2, "0", date.getMinutes());
    return ret;
}
function parse_weather(data){
    var pubT = new Date(data.current.pubTime);
    $('#weather>#today>.weather').text(weathercode[data.current.weather][0]);
    $('#weather>#tinfo>.aqi').text(dataLeftCompleting(3, " ", data.aqi.aqi));
    $('#weather>#today>.location').text(city);
    $('#weather>#today>.fresh').text(build_time(pubT));
    $('#weather>#today>.feel').text(parseFloat(data.current.feelsLike.value).toFixed(1));
    $('#weather>#today>.temp').text(dataLeftCompleting(3, " ", data.current.temperature.value)+"°C");
    $('#weather>#tinfo>.pressure').text(data.current.pressure.value);
    $('#weather>#tinfo>.hum').text(data.current.humidity.value);
    $('#weather>#tinfo>.wind').text(wind_level[parse_wind_level(data.current.wind.speed.value)]);
    $('.windd').text("\uf0b1");
    $('#weather>#tinfo>.windd').css({transform:"rotate("+data.current.wind.direction.value+"deg)"});
    var pubTime = new Date(data.forecastHourly.weather.pubTime);
    for(var i=0;i<4;i++){
        $('#today_forecast>#'+(i+1)+'h>.hint').text(build_time(new Date(pubTime.valueOf()+i*3600*1000)));    
        $('#today_forecast>#'+(i+1)+'h>.weather').text(weathercode[data.forecastHourly.weather.value[i]][0]);
        $('#today_forecast>#'+(i+1)+'h>.temp').text(dataLeftCompleting(3, " ", data.forecastHourly.temperature.value[i])+"°C");
        // $('#today_forecast>#1h>.wind').text(wind_level[parse_wind_level(data.forecastHourly.wind.value[0].speed)]);
        // $('#today_forecast>#1h>.windd').css({transform:"rotate("+data.forecastHourly.wind.value[0].direction+"deg)"});
        // $('#today_forecast>#1h>.aqi').text(data.forecastHourly.aqi.value[0]);
    }
    for(var j=0;j<3;j++){
        $('#forecast>#'+(j+1)+'d .weather1').text(weathercode[data.forecastDaily.weather.value[(j+1)].from][0]);
        $('#forecast>#'+(j+1)+'d .weather2').text(weathercode[data.forecastDaily.weather.value[(j+1)].to][0]);
        $('#forecast>#'+(j+1)+'d .temp1').text(data.forecastDaily.temperature.value[(j+1)].from);
        $('#forecast>#'+(j+1)+'d .temp2').text(data.forecastDaily.temperature.value[(j+1)].to);
        $('#forecast>#'+(j+1)+'d .wind').text(wind_level[parse_wind_level(data.forecastDaily.wind.speed.value[0].to)]);
        $('#forecast>#'+(j+1)+'d .aqi').text(dataLeftCompleting(3, " ", data.forecastDaily.aqi.value[(j+1)]));
        $('#forecast>#'+(j+1)+'d .wind').addClass(compare(data.forecastDaily.wind.speed.value[0].from,data.forecastDaily.wind.speed.value[0].to));        
    }
}
function update_weather(){
    $.ajax({
        url:'function/weather.php?city='+city,
        dataType:'json',
        processData: false, 
        type:'GET',
        success:function(data){
            parse_weather(data);
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.status);
            console.log(errorThrown);
            console.log(textStatus);
        }
    });
}
update_weather();
setInterval(update_weather,600000);