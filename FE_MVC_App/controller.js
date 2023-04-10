var data = ""
var current_plant = null
var current_plant_idx = 0

function init() {
    
    // Load data from backend
    data = getHttpAll();
    load_current_plant()

    if (data) {
        // Display 1st row
        display_weather_values();

        // Display 2nd box
        display_plant_detail_picture_user();
        display_plant_detail_status();
        display_plant_detail_information();


    }
}

function load_current_plant() {
    current_plant = {
        "node_id": data["plants_info"][0]['plant_node_id'],
        "name": data["plants_info"][0]['name'],
        "description": data["plants_info"][0]['description'],
        "disease": data["plants_info"][0]['disease'],
        "moisture": 0,
        "light": 0,
        "last_watered": "yesterday"
    }

    for (var plant in data['plant_sensor_data']) {
        if (plant['plant_node_id'] == current_plant['node_id']) {
            current_plant['moisture'] = plant['moisture'];
            current_plant['light'] = plant['light'];
        }
    }
}

function display_weather_values() {
    // Temperature
    var temp = Math.round(parseFloat(data.weather.temp.replace(',','.')) * 10) / 10;
    Circles.create({
        id: 'circles-1',
        radius: 45,
        value: temp,
        maxValue: 55,
        minValue: 0,
        width: 11,
        text: temp,
        colors: ['#eee', '#ab0505'],
        duration: 400,
        wrpClass: 'circles-wrp',
        textClass: 'circles-text',
        styleWrapper: true,
        styleText: true
    });

    // Humidity
    var humid = Math.round(parseFloat(data.weather.humidity.replace(',','.')) * 10) / 10;
    Circles.create({
        id: 'circles-2',
        radius: 45,
        value: humid,
        maxValue: 100,
        minValue: 0,
        width: 11,
        text: humid,
        colors: ['#eee', '#177dff'],
        duration: 400,
        wrpClass: 'circles-wrp',
        textClass: 'circles-text',
        styleWrapper: true,
        styleText: true
    });

    //Tank level
    var water_l = Math.round(parseFloat(data.water_tank.tank_level.replace(',','.'))) / 10;
    Circles.create({
        id: 'circles-3',
        radius: 45,
        value: water_l,
        maxValue: 100,
        minValue: 0,
        width: 7,
        text: water_l,
        colors: ['#eee', '#ab0505'],
        duration: 400,
        wrpClass: 'circles-wrp',
        textClass: 'circles-text',
        styleWrapper: true,
        styleText: true
    });
}


/*** Plant detail picture ***/
function onPlantDetailPictureButtonClick() {
    if (document.getElementById("PlantDetailPictureButton").className == "btn btn-primary btn-round"){
        display_plant_detail_picture_real();
    } else {
        display_plant_detail_picture_user();
    }

}

function display_plant_detail_picture_real() {
    document.getElementById("PlantDetailPictureButton").className = "btn btn-primary btn-border btn-round";
    p_b64 = ""
    for (var plant in data['plants_info']) {
        if (plant['plant_node_id'] == current_plant['node_id']) {
            p_b64 = plant['photo_url']
        }
    }

// Display 
}

function display_plant_detail_picture_user() {
    document.getElementById("PlantDetailPictureButton").className = "btn btn-primary btn-round";
    document.getElementById("PlantDetailPictureButton").src = "asset/img/plant_sense_icon";
}

function display_plant_detail_information() {
    document.getElementById("curr_plant_name").innerHTML = 
}

function display_plant_detail_status() {
    var disease = "no";
    var moisture = null;
    var light = null; 
    for (var plant in data['plants_info']) {
        if (plant['plant_node_id'] == current_plant['node_id']) {
            //disease = plant['disease'];
        }
    }

    for (var values in data['plant_sensor_data']) {
        if (values['plant_node_id'] == current_plant['node_id']) {
            moisture = values['moisture']
            light = values['light']
        }
    }

    // Health
    if (disease == "no") {
        Circles.create({
            id: 'circles-4',
            radius: 45,
            value: 1,
            maxValue: 1,
            minValue: 0,
            width: 45,
            colors: ['#eee', '#ab0505'],
            duration: 400,
            wrpClass: 'circles-wrp',
            styleWrapper: true,
        });
    } else {
        Circles.create({
            id: 'circles-4',
            radius: 45,
            value: 0,
            maxValue: 1,
            minValue: 0,
            width: 45,
            colors: ['#eee', '#ab0505'],
            duration: 400,
            wrpClass: 'circles-wrp',
            styleWrapper: true,
        });
    }

    // Moisture
    Circles.create({
        id: 'circles-5',
        radius: 45,
        value: moisture,
        maxValue: 1024,
        minValue: 0,
        width: 11,
        text: moisture,
        colors: ['#eee', '#177dff'],
        duration: 400,
        wrpClass: 'circles-wrp',
        textClass: 'circles-text',
        styleWrapper: true,
        styleText: true
    });

    // Light
    Circles.create({
        id: 'circles-6',
        radius: 45,
        value: light,
        maxValue: 256,
        minValue: 0,
        width: 11,
        text: light,
        colors: ['#eee', '#ab0505'],
        duration: 400,
        wrpClass: 'circles-wrp',
        textClass: 'circles-text',
        styleWrapper: true,
        styleText: true
    });    
}