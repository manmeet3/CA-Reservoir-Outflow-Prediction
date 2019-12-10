	var color = Chart.helpers.color;
	var barChartData = {
		labels: [{% for item in labels %}
		"{{item}}",
		{% endfor %}],
		datasets: [{
			type: 'bar',
			label: 'Urban Usage (maf)',
			backgroundColor: color(window.chartColors.blue).alpha(0.2).rgbString(),
			borderColor: window.chartColors.blue,
			data: [
			{% for x in usage %}
			{{x}},
			{% endfor %}
			],
		yAxisID: 'y-axis-1',	// ajout
	},	{
		type: 'line',
		label: 'Population (millions)',
		fill: false,
		borderColor: window.chartColors.red,
		data: [
		{% for x in pop %}
		{{x}},
		{% endfor %}
		],
	yAxisID: 'y-axis-2',	// ajout
	}]
	};

	// Define a plugin to provide data labels
	Chart.plugins.register({
	afterDatasetsDraw: function(chart) {
	var ctx = chart.ctx;

	chart.data.datasets.forEach(function(dataset, i) {
	var meta = chart.getDatasetMeta(i);
	if (!meta.hidden) {
		meta.data.forEach(function(element, index) {
			// Draw the text in black, with the specified font
			ctx.fillStyle = 'rgb(0, 0, 0)';

			var fontSize = 12;
			var fontStyle = 'bold';
			var fontFamily = 'Helvetica Neue';
			ctx.font = Chart.helpers.fontString(fontSize, fontStyle, fontFamily);

			// Just naively convert to string for now
			var dataString = dataset.data[index].toString();

			// Make sure alignment settings are correct
			ctx.textAlign = 'center';
			ctx.textBaseline = 'middle';

			var padding = 5;
			var position = element.tooltipPosition();
			ctx.fillText(dataString, position.x, position.y - (fontSize / 2) - padding);
		});
	}
	});
	}
	});


	window.onload = function() {
	var ctx = document.getElementById('canvas').getContext('2d');
	window.myBar = new Chart(ctx, {
	type: 'bar',
	data: barChartData,
	options: {
	responsive: true,
	title: {
		display: false,
		text: 'Population vs water consumption'
	},
	scales: {
		yAxes: [{
			type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
			display: true,
			position: 'left',
			id: 'y-axis-1',
		}, {
			type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
			display: true,
			position: 'right',
			id: 'y-axis-2',

			// grid line settings
			gridLines: {
				drawOnChartArea: false, // only want the grid lines for one axis to show up
			},
		}],
	}
	}
	});

	var otx = document.getElementById('outflowChart').getContext('2d');

	var myChart = new Chart(otx, {
    type: 'line',
    data: {
        labels: [{% for item in outflow['labels'] %}
		"{{item}}",
		{% endfor %}],
        datasets: [{
            label: 'actual outflow',
            data: [
			{% for x in outflow['actuals'] %}
			{{x}},
			{% endfor %}
			],
		    fill: false,
            pointRadius: 2,
            backgroundColor: "rgba(0, 0, 0, 0.5)",
            borderColor: "rgba(0, 0, 0, 0.0)",
            borderWidth: 1
        },
       {
            label: 'predicted outflow',
            data: [
			{% for x in outflow['predicted'] %}
			{{x}},
			{% endfor %}
			],
		    fill: false,
		    radius: 0,
            pointRadius: 0,
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor:'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});

	};
