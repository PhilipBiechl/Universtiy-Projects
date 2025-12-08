/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

/* temperature */
let istTemp = 0;
let sollTemp = 0;
let regTemp = 0;
let lastTemp = [0, 0];

/* temperature data for chart */
let temperatureData = []; 
const maxDataPoints = 36; 

/* variables for other values to update */
let wantedTemperature = 0.0; 
let regulatedTemperature = 0.0; 
let regulateMode = false; 
let otherValues = {
    humidity: 0,      
    simM: 0,    
    regM: 0,  
    ssid: '',   
    devicename: ''  
};

/* ctrl for connection state */
let ctrl_cnt = [0, -1];
let connState = 0;

/* controller parameters */
let ki = 0;
let kp = 0;

/* "enum" for display of connection status */
const Connection = {
    ON: 1,
    OFF: 0
}

/* update values from esp */
function dataRcv() {
    fetch('/data').then(response => {
        return response.text();
    }).then(data => {
        let felder = data.split(',', 11);
        istTemp = parseFloat(felder[0]);
        sollTemp = parseFloat(felder[1]);
        regTemp = parseFloat(felder[2]);
        otherValues.humidity = parseFloat(felder[3]);
        otherValues.simM = parseFloat(felder[4]);
        otherValues.regM = parseFloat(felder[5]);
        otherValues.ssid = felder[6];
        otherValues.devicename = felder[7];
        ctrl_cnt[0] = felder[8];
        ki = parseFloat(felder[9]);
        kp = parseFloat(felder[10]);
    });
}

/* change regulation on <-> off */
function toggleReg() {
    fetch('/reg');
}

/* change simulation on <-> off */
function toggleSim() {
    fetch('/sim');
}

/* listen for button to send controller parameters to esp */
document.getElementById('sendDataButton').addEventListener('click', async () => {
    const field1 = document.getElementById('field1').value;
    const field2 = document.getElementById('field2').value;

    if (!field1 || !field2) {
        alert('Please fill in both fields');
        return;
    }
    if (parseFloat(field1) > 10 || parseFloat(field2) > 10) {
        alert('Maximum for control parameters is 10');
        return;
    }
    if (parseFloat(field1) < 0 || parseFloat(field2) < 0) {
        alert('No negative control parameters allowed');
        return;
    }

    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ field1, field2 }),
        });

        if (response.ok) {
            const data = await response.text();
            if (data == "1") {
                document.getElementById("response-message").style.display = "block";
            } else {
                alert(data);
            }
        } else {
            alert('Error: Unable to send data');
        }
    } catch (error) {
        alert('Error: Could not reach the server');
    }
});

/* show pulsating red dot */
function showLiveIndicator(isLive) {
    const liveDot = document.querySelector('.live-dot');
    if (isLive) {
        liveDot.style.display = 'inline-block'; // Show the live dot
    } else {
        liveDot.style.display = 'none'; // Hide the live dot if not live
    }
}

/* listen for change of content view in main view of webpage */
document.addEventListener("DOMContentLoaded", () => {
    const dropdown = document.getElementById("dropdown");

    const contentMap = {
        option1: document.getElementById("content1"),
        option2: document.getElementById("content2"),
        option3: document.getElementById("content3"),
    };

    dropdown.addEventListener("change", () => {
        const selectedOption = dropdown.value;

        Object.values(contentMap).forEach((section) => {
            section.style.display = "none";
        });

        if (contentMap[selectedOption]) {
            contentMap[selectedOption].style.display = "block";
        }
    });

    dropdown.dispatchEvent(new Event("change"));
});

/* get chart to desired size */
function resizeChart(width, height) {
    const canvas = document.getElementById('temperatureChart');
    
    canvas.style.width = `${width}vw`;
    canvas.style.height = `${height}vh`;

    temperatureChart.resize();
}

/* check if simulation is on */
function get_gSimMode() {
    fetch('/gSimMode').then(response => {
        return response.text();
    }).then(data => {
        otherValues.status = data;
    });
}

/* Simulated temperature update (every second) */
function updateTemperature() {
    const currentTemperature = istTemp;
    const currentSollwert = sollTemp;
    const regulatedTemperature = regTemp;
    const timestamp = new Date().toLocaleString('de-DE');

    temperatureData.push({
        timestamp,
        temperature: currentTemperature,
        wanted: currentSollwert,
        regulated: regulatedTemperature
    });

    /* keep only a specific amount of datapoints */
    if (temperatureData.length > maxDataPoints) {
        temperatureData.shift(); 
    }

    if (ctrl_cnt[0] == ctrl_cnt[1]) {
        connState = Connection.OFF;
    } else {
        ctrl_cnt[1] = ctrl_cnt[0]
        connState = Connection.ON;
    }

    lastTemp[1] = lastTemp[0];
    lastTemp[0] = currentTemperature;

    get_gSimMode();
    dataRcv();
    updateUI();
    updateChart();
}

/* Start updating temperature every second */
setInterval(updateTemperature, 1000);

/* update ui text & other elements */
function updateUI() {
    if (connState == Connection.OFF) {
        document.getElementById("conn-off").style.display = "block";
        document.getElementById("conn-on-0").style.display = "none";
        document.getElementById("conn-on-1").style.display = "none";
        document.getElementById("conn-on-2").style.display = "none";
    } else {
        document.getElementById("conn-off").style.display = "none";
        document.getElementById("conn-on-0").style.display = "block";
        document.getElementById("conn-on-1").style.display = "block";
        document.getElementById("conn-on-2").style.display = "block";
    }

    document.getElementById("response-message").style.display = "none";

    document.getElementById('device-name').textContent = "Displayed here to track temperature regulated by the device: " + otherValues.devicename;
    document.getElementById('currentTemperature').textContent = temperatureData.length ? temperatureData[temperatureData.length - 1].temperature.toFixed(1) : '--';
    document.getElementById('wantedTemperature').textContent = temperatureData.length ? temperatureData[temperatureData.length - 1].wanted.toFixed(1) : '--';
    document.getElementById('regulatedTemperature').textContent = temperatureData.length ? temperatureData[temperatureData.length - 1].regulated.toFixed(1) : '--';

    document.getElementById("rotor-1").style.transform = `rotate(${((regTemp + 20) * 5 - 150)}deg)`;
    document.getElementById("rotor-2").style.transform = `rotate(${((regTemp + 20) * 5 - 150)}deg)`;

    document.getElementById("heater").style.backgroundColor = `rgb(${(regTemp+30)*2}, 0, ${(150 - ((regTemp+30)*2) + 30)})`;
    document.getElementById("room").style.backgroundColor = `rgb(${(istTemp+30)*2}, 0, ${(150 - ((istTemp+30)*2) + 30)})`;

    document.getElementById('humidityValue').textContent = otherValues.humidity.toFixed(2);
    document.getElementById('simValue').textContent = (otherValues.simM != 0 ? "active" : "off");
    document.getElementById('regValue').textContent = (otherValues.regM != 0 ? "active" : "off");
    document.getElementById('ssidValue').textContent = otherValues.ssid;
    document.getElementById('deviceValue').textContent = otherValues.devicename;

    document.getElementById('pid').textContent = `Current values: sensitivity: ${ki.toFixed(1)}, deflection: ${kp.toFixed(1)}`;
}

/* Initialize the 'Chart.js' line chart */
const ctx = document.getElementById('temperatureChart').getContext('2d');
const temperatureChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], // Timestamps
        datasets: [
            {
                label: 'Temperature',
                data: [], // Temperature values
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true
            },
            {
                label: 'Desired Temperature',
                data: [], // Temperature values
                borderColor: 'rgba(75, 120, 100, 1)',
                backgroundColor: 'rgba(75, 120, 100, 0.2)',
                fill: true
            },
        ]
    },
    options: {
        animations: {
            radius: {
              duration: 400,
              easing: 'linear',
              loop: (context) => context.active
            }
        },
        hoverRadius: 12,
        hoverBackgroundColor: 'yellow',
        interaction: {
            mode: 'nearest',
            intersect: false,
            axis: 'x'
        },
        plugins: {
            tooltip: {
                enabled: false
            }
        },
        responsive: true,
        maintainAspectRatio: true,
        scales: {
            x: {
                type: 'minute',
                time: {
                    unit: 'hour'
                },
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Temperature (°C)'
                },
                suggestedMin: 0,
                suggestedMax: 30
            }
        },
    }
});

/* update chart data when new data from esp is received */
function updateChart() {
    resizeChart(75, 60);

    const timestamps = temperatureData.map(data => data.timestamp);
    const temperatures = temperatureData.map(data => data.temperature);
    const sollwert = temperatureData.map(data => data.wanted);

    temperatureChart.data.labels = timestamps;
    temperatureChart.data.datasets[0].data = temperatures;
    temperatureChart.data.datasets[1].data = sollwert;
    temperatureChart.update();
}