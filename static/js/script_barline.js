document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    console.log(file);
    if (file && file.type === 'text/csv') {
        const reader = new FileReader();
        reader.onload = function(e) {
            const csvText = e.target.result;
            parseAndCreateChart(csvText);
            console.log(csvText.length);
        };
        reader.readAsText(file);
    } else {
        alert('Please select a valid CSV file.');
    }
});

function parseAndCreateChart(csvText) {
    // Parsing the CSV data
    const lines = csvText.split('\n');
    const headers = lines[0].split(',');

    const dates = [];
    const ambientTemps = [];
    const moduleTemps = [];
    const sunHours = [];
    const yields = [];

    for (let i = 1; i < lines.length; i++) {
        const data = lines[i].split(',');
        if (data.length === headers.length) {
            dates.push(data[0]);
            ambientTemps.push(parseFloat(data[1]));
            moduleTemps.push(parseFloat(data[2]));
            sunHours.push(parseFloat(data[3]));
            yields.push(parseInt(data[4]));
        }
    }

    // Creating the chart with vertical bars and horizontal lines
    const ctx = document.getElementById('myChart').getContext('2d');
//    const newTab = window.open();
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Yield (J)',
                    type: 'bar',
                    data: yields,
                    backgroundColor: 'rgba(255, 206, 86, 0.2)',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 1,
                    yAxisID: 'y-axis-1'
                },
                {
                    label: 'Ambient Temp (°C)',
                    type: 'line',
                    data: ambientTemps,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false,
                    yAxisID: 'y-axis-2'
                },
                {
                    label: 'Module Temp (°C)',
                    type: 'line',
                    data: moduleTemps,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    fill: false,
                    yAxisID: 'y-axis-2'
                },
                {
                    label: 'Sun Hours',
                    type: 'line',
                    data: sunHours,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    fill: false,
                    yAxisID: 'y-axis-2'
                }
            ]
        },
        options: {
            scales: {
                yAxes: [
                    {
                        id: 'y-axis-1',
                        type: 'linear',
                        position: 'left',
                        ticks: {
                            beginAtZero: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Yield'
                        }
                    },
                    {
                        id: 'y-axis-2',
                        type: 'linear',
                        position: 'right',
                        ticks: {
                            beginAtZero: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Temperature (°C) / Sun Hours'
                        }
                    }
                ],
                xAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'Date'
                        }
                    }
                ]
            }
        }
    });
}
