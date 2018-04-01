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
    <link rel="stylesheet" href="css/time.css"/>
    <link rel="stylesheet" href="css/weather.css"/>
    <script src="js/weather.js"></script>
</head>
<body>
    <div class="top left" id='datetime'>
        <div id="date">
            <span id="year">2018</span><span id="month"> 3</span><span id="day">31</span><span id="week">礼拜六</span><br>
            <span id="lunar"></span>
        </div>
        <div id="time">
            <span id="hour">00</span><span id="minute">00</span><span id="second">00</span>
        </div>
    </div>
    <div class="top right" id="weather">
        <div id="today">
            <span class="fresh">00:00</span>
            <span class="weather">+</span><span class="temp">00</span><span class="feel">00.0</span>
        </div>
        <div id="tinfo">
            <div class="windd"></div><span class="wind"></span><span class="pressure">1000</span><span class="hum">50</span><span class="aqi">0</span>            
        </div>
        <div id="forecast"></div>
    </div>
</body>
</html>