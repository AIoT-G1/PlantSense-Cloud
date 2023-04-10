var data = ""

function init() {
    
    // Load data from backend
    data = getHttpAll();
    if (data) {
        // Display 1st row
        display_weather_values();

        // Display 2nd box
        display_plant_info_section


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