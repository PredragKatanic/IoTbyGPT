const currentDataUrl = "http://127.0.0.1:8000/api/measurements/latest";
const recentDataUrl = "http://127.0.0.1:8000/api/measurements/";

async function fetchCurrentData() {
    try {
        const response = await fetch(currentDataUrl);
        const data = await response.json();
        
        document.getElementById("temperature").textContent = data.temperature.toFixed(1);
        document.getElementById("humidity").textContent = data.humidity.toFixed(1);
        document.getElementById("measurement-time").textContent = 
            `Measurement Time: ${new Date(data.measurement_time).toLocaleString()}`;
    } catch (error) {
        console.error("Error fetching current data:", error);
    }
}

async function fetchRecentData() {
    try {
        const response = await fetch(recentDataUrl);
        const data = await response.json();

        const labels = data.map(item => new Date(item.measurement_time).toLocaleTimeString());
        const temperatures = data.map(item => item.temperature);
        const humidities = data.map(item => item.humidity);

        updateChart(labels, temperatures, humidities);
    } catch (error) {
        console.error("Error fetching recent data:", error);
    }
}

function updateChart(labels, temperatures, humidities) {
    const ctx = document.getElementById('measurementChart').getContext('2d');

    if (window.myChart) {
        window.myChart.destroy();
    }

    window.myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: temperatures,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    fill: false,
                    yAxisID: 'y'
                },
                {
                    label: 'Humidity (%)',
                    data: humidities,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    fill: false,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    }
                },
                y1: {
                    beginAtZero: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Humidity (%)'
                    }
                }
            }
        }
    });
}

function init() {
    fetchCurrentData();
    fetchRecentData();

    setInterval(() => {
        fetchCurrentData();
        fetchRecentData();
    }, 60000);
}

document.addEventListener("DOMContentLoaded", init);
