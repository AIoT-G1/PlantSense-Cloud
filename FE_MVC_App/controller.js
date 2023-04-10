var data = ""
var current_plant_node_id = ""

function init() {
    
    // Load data from backend
    data = getHttpAll();
    if (data) {
        // Display 1st row
        display_weather_values();

        // Display 2nd box
        display_plant_detail_picture_user()


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
        colors: ['#00cde8', '#ab0505'],
        duration: 400,
        wrpClass: 'circles-wrp',
        textClass: 'circles-text',
        styleWrapper: true,
        styleText: true
    });
}


// Plant detail picture
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
        if (plant['plant_node_id'] == current_plant_node_id) {
            p_b64 = plant['photo_url']
        }
    }

    // Display 
}

function display_plant_detail_picture_user() {
    document.getElementById("PlantDetailPictureButton").className = "btn btn-primary btn-round";
    document.getElementById("PlantDetailPictureButton").src = "asset/img/plant_sense_icon";
}