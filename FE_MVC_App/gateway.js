const url = 'http://127.0.0.1:5000/';

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


// POST
function postHttpEventMessage(data){
    my_events = ""
    $.ajax({
        url : url + '/events',
        type : 'POST',
        data: {'data': JSON.stringify(data)},
        async: false,
        crossDomain:true,
        'success' : function(response) {
            my_events = JSON.parse(response);
            console.log("Event triggered successfully")
        },
        'error' : function(request,error)
        {
            console.log("Event trigger failed")
        }
    });
    return my_events;
}
