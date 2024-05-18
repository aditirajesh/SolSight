document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file && file.type === 'text/csv') {
        const reader = new FileReader();
        reader.onload = function(e) {
            const csvText = e.target.result;
            parseAndCreateChart(csvText);
        };
        reader.readAsText(file);
    } else {
        alert('Please select a valid CSV file.');
    }
});

function parseAndCreateChart(csvText) {
    // Parsing the CSV data
//    const lines = csvText.split('\n');
// Reading the CSV file
// fetch('http://localhost:8000/data1_1.csv')
//    .then(response => response.text())
//    .then(csvText => {
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
            dates.push(data[0]);
            ambientTemps.push(parseFloat(data[1]));
            moduleTemps.push(parseFloat(data[2]));
            sunHours.push(parseFloat(data[3]));
            yields.push(parseFloat(data[4]));
        }

        // Creating the bar chart with multiple lines
        const ctx = document.getElementById('myChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'Ambient Temp (°C)',
                        data: ambientTemps,
                        backgroundColor: 'rgba(27, 255, 0, 0.8)',
                        borderColor: 'rgba(27, 255, 0, 1)',
                        borderWidth: 1,
                        yAxisID: 'y-axis-1'
                    },
                    {
                        label: 'Module Temp (°C)',
                        data: moduleTemps,
                        backgroundColor: 'rgba(123, 0, 0, 0.8)',
                        borderColor: 'rgba(123, 0, 0, 1)',
                        borderWidth: 1,
                        yAxisID: 'y-axis-1'
                    },
                    {
                        label: 'Sun Hours',
                        data: sunHours,
                        backgroundColor: 'rgba(31, 0, 255, 0.8)',
                        borderColor: 'rgba(31, 0, 255, 1)',
                        borderWidth: 1,
                        yAxisID: 'y-axis-2'
                    },
                    {
                        label: 'Yield (J)',
                        data: yields,
                        backgroundColor: 'rgba(255, 0, 0, 0.8)',
                        borderColor: 'rgba(255, 0, 0, 1)',
                        borderWidth: 1,
                        yAxisID: 'y-axis-3'
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
                                labelString: 'Temperature (°C)'
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
                                labelString: 'Sun Hours'
                            }
                        },
                        {
                            id: 'y-axis-3',
                            type: 'linear',
                            position: 'right',
                            ticks: {
                                beginAtZero: true
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Yield'
                            }
                        }
                    ]
                }
            }
        });
}