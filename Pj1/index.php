<!DOCTYPE html>
<html lang="zh_CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>My</title>
    <script src="js/jquery.js"></script>
    <script src="js/lunar.js"></script>
    <script src="js/time.js"></script>
    <script src="js/weather.js"></script>
    <script src="js/jquery.qrcode.js"></script>
    <script src="js/messages.js"></script>
    <link rel="stylesheet" href="css/time.css"/>
    <link rel="stylesheet" href="css/weather.css"/>
    <link rel="stylesheet" href="css/messages.css"/>
</head>
<body>
    <div class="top left" id='datetime'>
        <div id="date">
            <span id="year">2018</span><span id="month"> 3</span><span id="day">31</span><span id="week">礼拜六</span>
        </div>
        <div id="time">
            <span id="hour">00</span><span id="minute">00</span><span id="second">00</span>
        </div>
        <div id="lunar"></div>
    </div>
    <div class="top right" id="weather">
        <div id="today">
            <span class="fresh">00:00</span><span id="locate">宝山</span>
            <span class="weather">+</span><span class="temp">00</span><span class="feel">00.0</span>
        </div>
        <div id="tinfo">
            <div class="windd"></div><span class="wind"></span><span class="pressure">1000</span><span class="hum">50</span><span class="aqi">0</span>            
        </div>
        <div id="today_forecast">
            <div id="4h"><span class='hint'>4小时</span><br><span class="weather">+</span><span class="temp">00</span></div>
            <div id="3h"><span class='hint'>3小时</span><br><span class="weather">+</span><span class="temp">00</span></div>
            <div id="2h"><span class='hint'>2小时</span><br><span class="weather">+</span><span class="temp">00</span></div>
            <div id="1h"><span class='hint'>1小时</span><br><span class="weather">+</span><span class="temp">00</span></div>
        </div>
        <div id="forecast">
            <div id="1d">
                <span class='hint'>明天</span><span class="wind"></span><div class="temp"><span class="temp1">00</span><span class="temp2">00</span></div>
                <span class="aqi">0</span>
                <div class="weather">
                    <span class="weather1">+</span><span class="weather2">+</span>
                </div>
            </div><br>
            <div id="2d">
                <span class='hint'>后天</span><span class="wind"></span><div class="temp"><span class="temp1">00</span><span class="temp2">00</span></div>
                <span class="aqi">0</span>
                <div class="weather">
                    <span class="weather1">+</span><span class="weather2">+</span>
                </div>
            </div><br>
            <div id="3d">
                <span class='hint'>大后天</span><span class="wind"></span><div class="temp"><span class="temp1">00</span><span class="temp2">00</span></div>
                <span class="aqi">0</span>
                <div class="weather">
                    <span class="weather1">+</span><span class="weather2">+</span>
                </div>
            </div>
        </div>
    </div>
    <div class="top right" id="noweather" style='display:none;'>
    天气信息刷新失败
    </div>
    <div class="bottom" id='messages'>
        <div class="weatherInfo"></div>
        <div class="message">
            <div class="title">这里是标题</div>
            <span class="content">这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容这里是内容</span>
            <div class="qrcode" data="https://www.baidu.com/"></div>
        </div>
    </div>
</body>
</html>