
function show_messages(){
    if ($('#messages>.message').length > 0){
        if ($('#messages>.activate').length > 0){
            var next = $('#messages>.activate').next('.message');
            if (next.length==0){
                $('#messages>.activate').removeClass('activate');
                update_message();
            }else{
                $('#messages>.activate').removeClass('activate');
                next.addClass('activate');
            }
        }else{
            $('#messages>.message').first('.message').addClass('activate');
        }
        if ($('#messages>.activate>.qrcode').length > 0){
            if ($('#messages>.activate>.qrcode>canvas').length == 0){
                $('#messages>.activate>.qrcode').qrcode($('#messages>.activate>.qrcode').attr('data'));
            }
        }
    }
}
function update_message(){
    $.ajax({
        url:'function/rss.php',
        dataType:'text',
        processData: false, 
        type:'GET',
        success:function(d){
            $('#messages').html(d);
            show_messages();
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.status);
            console.log(errorThrown);
            console.log(textStatus);
        }
    });
}
update_message();
setInterval(show_messages,60000);
