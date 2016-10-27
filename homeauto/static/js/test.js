$(document).ready(function() {
    $('#simple-menu').sidr({
        displace: false
    });
    
    $("#controller").click(function() {
            $.sidr('close');
    });

});

//Set initial Status for Devices
Onkyo_Power_Status();
Projector_Power_Status();

function Onkyo_Power_Status(){
    $.ajax({
        url: "http://10.10.10.9:5000/api/v1/onkyo/onkyo_pwr?pwr=query",
    }).done(function(data){
        switch(data){
        case 'standby':
            $("#onkyo_pwr").text('Power Onkyo On');
            $("#onkyo_pwr").attr('onclick', 'toggle_onkyo_pwr("on")');
            break;
        case 'on':
            $("#onkyo_pwr").text('Power Onkyo Off');
            $("#onkyo_pwr").attr('onclick', 'toggle_onkyo_pwr("standby")');
            break;
        }
    });
}

function Projector_Power_Status(){
    $.ajax({
        url: "http://10.10.10.9:5000/api/v1/projector/proj_power?pwr=?",
    }).done(function(data){
        switch(data.split("*")[2].split("#")[0]){
        case 'POW=OFF':
            $("#proj_pwr").text('Power Projector On');
            $("#proj_pwr").attr('onclick', 'toggle_projector_pwr("on")');
            break;
        case 'POW=ON':
            $("#proj_pwr").text('Power Projector Off');
            $("#proj_pwr").attr('onclick', 'toggle_projector_pwr("off")');
            break;
        default:
            setTimeout(function() {}, 1000);
            $("#proj_pwr").text('Projector Status Updating...');
            Projector_Power_Status();
        }
    });
}

function toggle_onkyo_pwr(state){
    $.ajax({
        url: "http://10.10.10.9:5000/api/v1/onkyo/onkyo_pwr?pwr=" + state,
    }).done(function(){
        Onkyo_Power_Status();
    });
}

function toggle_projector_pwr(state){
    $.ajax({
        url: 'http://10.10.10.9:5000/api/v1/projector/proj_power?pwr=' + state,
    }).done(function(){
        Projector_Power_Status();
    });
}

function connect_to_firetv(ipaddy){
    //ajax call to routable address
}

function control_firetv(command){
    //ajax call to routable address to call adb commands for up/down/left/right/etc
}

