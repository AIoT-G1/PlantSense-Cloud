const url = "http://172.25.107.100:5000"

// GET
function getHttpSensorValues(){
    var data = null;
    $.ajax({
        url : url + '/sensor_values',
        type : 'GET',
        async: false,
        crossDomain:true,
        'success' : function(response) {
            data = JSON.parse(response);
        },
        'error' : function(request,error)
        {
            console.log("Request: "+JSON.stringify(request));
        }
    });
    return data;
}

function getHttpPlantData() {
    var data = null;

    $.ajax({
        url: url + '/plant_data',
        type: 'GET',
        async: false,
        crossDomain: true,
        'success': function (response) {
            data = JSON.parse(response);
        },
        'error': function (request, error) {
            console.log("Request: " + JSON.stringify(request));
        }
    });

    return data;
}

function getHttpAll() {
    var data = null;
    $.ajax({
        url: url + '/all',
        type: 'GET',
        async: false,
        crossDomain: true,
        'success': function (response) {
            data = JSON.parse(response);
        },
        'error': function (request, error) {
            console.log("Request: " + JSON.stringify(request));
        }
    });

    return data;
}

// Post methods
function postHttpPlantInformation(data){
    res = ""
    $.ajax({
        url : url + '/plant_info',
        type : 'POST',
        data: {'data': JSON.stringify(data)},
        async: false,
        crossDomain:true,
        'success' : function(response) {
            res = JSON.parse(response);
            console.log("Event triggered successfully")
        },
        'error' : function(request,error)
        {
            console.log("Event trigger failed")
        }
    });
    return res;
}
