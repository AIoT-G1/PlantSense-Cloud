var data = ""
var current_plant = {
    "node_id": "",
    "name": "",
    "description": "",
    "disease": "",
    "breed": "",
    "moisture": 0,
    "light": 0,
    "photo_url": "",
    "water_history": []
}
var current_plant_idx = 0

function init() {
    
    // Load data from backend
    data = getHttpAll();
    load_current_plant();

    if (data) {
        // Display 1st row
        display_weather_values();

        // Display 2nd box
        display_plant_detail_picture_user();
        display_plant_detail_status();
        display_plant_detail_information();


    }
}

// Load data
function load_current_plant() {
    debugger;
    if (data["plants_info"].length > 0) {
        if (data["plants_info"][current_plant_idx].hasOwnProperty("plant_node_id")) {
            current_plant["node_id"] = data["plants_info"][current_plant_idx]['plant_node_id']
        } else {
            current_plant["Unknown"]
        }
        if (data["plants_info"][current_plant_idx].hasOwnProperty("name")) {
            current_plant["name"] = data["plants_info"][current_plant_idx]['name']
        } else {
            current_plant["name"] = "Unknown"
        }
        if (data["plants_info"][current_plant_idx].hasOwnProperty("description")) {
            current_plant["description"] = data["plants_info"][current_plant_idx]['description']
        }
        else {
            current_plant["description"] = "Unknown"
        }
        if (data["plants_info"][current_plant_idx].hasOwnProperty("disease")) {
            current_plant["disease"] = data["plants_info"][current_plant_idx]['disease']
        } else {
            current_plant["disease"] = "Unknown"
        }
        if (data["plants_info"][current_plant_idx].hasOwnProperty("breed")) {
            current_plant["breed"] = data["plants_info"][current_plant_idx]['breed']
        } else {
            current_plant["breed"] = "Unknown"
        } 
        if (data["plants_info"][current_plant_idx].hasOwnProperty("water_history")) {
            if (data["plants_info"][current_plant_idx]['water_history'].length == 0) {
                current_plant['water_history'] = data["plants_info"][current_plant_idx]['water_history']
            }
        } else {
            current_plant['water_history'] = []
        }
        if (data["plants_info"][0].hasOwnProperty("photo_url")) {
            current_plant["photo_url"] = data["plants_info"][current_plant_idx]['photo_url']
        } else {
            current_plant['photo_url'] = "assets\\img\\unavailable.jpg"
        }
    }
    
    if (data['plant_sensor_data'].length > 0) {
        var moisture = ""
        var light = ""
        for (var i = 0; i < data['plant_sensor_data'].length; i++){
            if (data['plant_sensor_data'][i]['plant_node_id'] == current_plant['node_id']) {
                moisture = data['plant_sensor_data'][i]['moisture'];
                light = data['plant_sensor_data'][i]['light'];
            }
        }
        debugger;
        if (moisture == "") {
            moisture = "0"
        }
        if (light == "") {
            light = "0"
        }
        current_plant['light'] = light
        current_plant['moisture'] = moisture 
    }
}


// Add / Edit
function onAddPlantButtonClick() {
    $("#update-plant-nodeId").val("");
    $("#update-plant-name").val("");
    $("#update-plant-desc").val("");
    $("#update-plant-breed").val("");
}

function onEditPlantButtonClick(){
    $("#update-plant-nodeId").val(current_plant['node_id']);
    $("#update-plant-name").val(current_plant['name']);
    $("#update-plant-desc").val(current_plant['description']);
    $("#update-plant-breed").val(current_plant['breed']);
}

function onSavePlantInformationModalButtonClick(){
    let node_id = $("#update-plant-nodeId").val();
    let name = $("#update-plant-name").val();
    let desc = $("#update-plant-desc").val();
    let breed = $("#update-plant-breed").val();

    //debugger;
    plant_data = {
        "plant_node_id": node_id,
        "name": name,
        "description": desc,
        "breed": breed,
        "disease": "no"
    }
    postHttpPlantInformation(plant_data);
    data = getHttpAll();
    load_current_plant();

    $("#update-plant-nodeId").val("");
    $("#update-plant-name").val("");
    $("#update-plant-desc").val("");
    $("#update-plant-breed").val("");

}

// Weather conditions
function display_weather_values() {
    if (data['weather'] != null) {
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
    document.getElementById("PlantDetailPicture").src = current_plant['photo_url']
}

function display_plant_detail_picture_user() {
    document.getElementById("PlantDetailPictureButton").className = "btn btn-primary btn-round";
    document.getElementById("PlantDetailPicture").src = current_plant['photo_url']
}

function display_plant_detail_information() {
    //debugger;
    document.getElementById("curr_plant_nodeID").innerText = current_plant['node_id']
    document.getElementById("curr_plant_name").innerText = current_plant['name']
    document.getElementById("curr_plant_desc").innerText = current_plant['description']
    document.getElementById("curr_plant_breed").innerText = current_plant['breed']
    document.getElementById("curr_plant_disease").innerText = current_plant['disease']

    if (current_plant.hasOwnProperty("water_history")) {
        debugger;
        if (current_plant["water_history"].length > 0) {
            last_rec = current_plant["water_history"].length - 1;
            document.getElementById("curr_plant_last_wat").innerText = current_plant['water_history'][last_rec]
        }
        else {
            document.getElementById("curr_plant_last_wat").innerText = "None"
        }
    }
}

function display_plant_detail_status() {
    // Moisture
    Circles.create({
        id: 'circles-5',
        radius: 45,
        value: current_plant['moisture'],
        maxValue: 1024,
        minValue: 0,
        width: 11,
        text: current_plant['moisture'],
        colors: ['#eee', '#336600'],
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
        value: current_plant['light'],
        maxValue: 256,
        minValue: 0,
        width: 11,
        text: current_plant['light'],
        colors: ['#eee', '#cccc00'],
        duration: 400,
        wrpClass: 'circles-wrp',
        textClass: 'circles-text',
        styleWrapper: true,
        styleText: true
    });    
}

function onPlantDetailNavigationPreviousClick() {
    if (current_plant_idx > 0) {
        current_plant_idx = current_plant_idx-1
        load_current_plant()
        document.getElementById("current-plant-nav-index").innerHTML = current_plant_idx + 1  
        display_plant_detail_information()
        display_plant_detail_status()
    }
}

function onPlantDetailNavigationNextClick() {
    if (current_plant_idx < data['plants_info'].length - 1) {
        current_plant_idx = current_plant_idx+1
        load_current_plant()
        document.getElementById("current-plant-nav-index").innerHTML = current_plant_idx + 1 
        display_plant_detail_information()
        display_plant_detail_status()
    }
}