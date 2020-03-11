// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var obj = document.getElementById("hbar-chart");
var chart = new Chart(obj, {
    type:'horizontalBar',
    data: {
        labels: ['Documentos', 
                'Página de bienvenida', 
                'Crear base de datos', 
                'Página Login',
                'Reuniones'
        ],
        datasets: [
            {
                label:'Tiempo invertido',
                data: [ 200,
                        50,
                        20,
                        60,
                        100
                ],
                backgroundColor: "rgba(250, 154, 67,1)",
                
                order:-99
            },
            
        ]
        

    },
    options:{
        maintainAspectRatio: false,
        legend:{
            display:false,
            labels:{
                display:false,
                fontSize:10000
            }
        },
        scales: {
            yAxes: [{
                barThickness: 20,
                ticks: {
                    beginAtZero:true,
                    
                    z:99
                    
                },
                
                gridLines:{
                    display:false
                }
            }],
            xAxes: [{
                ticks: {
                    beginAtZero:true,  
                    z:99
                },
                gridLines: {
                    display:false
                }
            }]
        },
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            titleMarginBottom: 10,
            titleFontColor: '#6e707e',
            titleFontSize: 14,
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            intersect: false,
            mode: 'index',
            caretPadding: 10,
            callbacks: {
              label: function(tooltipItem, chart) {
                var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                return datasetLabel + ': ' + number_format(tooltipItem.xLabel);
              }
            }
        },
        
    }

});












