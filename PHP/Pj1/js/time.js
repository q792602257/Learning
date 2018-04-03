function dataLeftCompleting(bits, identifier, value){
    value = Array(bits + 1).join(identifier) + value;
    return value.slice(-bits);
}
var week = ["礼拜天","礼拜一","礼拜二","礼拜三","礼拜四","礼拜五","礼拜六"];
function update_datetime(){
    var time = new Date();
    var lunar = calendar.solar2lunar(time.getFullYear(),(time.getMonth()+1),time.getDate());
    $("#lunar").text(lunar.IMonthCn+lunar.IDayCn);
    $("#year").text(time.getFullYear());
    $("#month").text(dataLeftCompleting(2, " ", (time.getMonth()+1)));
    $("#day").text(dataLeftCompleting(2, "  ", time.getDate()));
    $("#week").text(week[time.getDay()]);
    $("#hour").text(dataLeftCompleting(2, "0", time.getHours()));
    $("#minute").text(dataLeftCompleting(2, "0", time.getMinutes()));
    $("#second").text(dataLeftCompleting(2, "0", time.getSeconds()));
}
update_datetime();
setInterval(update_datetime,1000);