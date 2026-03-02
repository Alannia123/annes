// ai_ama/static/src/js/ai_chart.js
/* global Plotly, window */
(function () {
    "use strict";

    function renderChart(chartData) {
        if (!chartData || !chartData.x || !chartData.series) {
            return;
        }
        var traces = chartData.series.map(function (s) {
            return {
                x: chartData.x,
                y: s.data,
                type: 'bar',
                name: s.name
            };
        });

        var layout = {
            barmode: 'group',
            margin: { t: 40, b: 120 },
            xaxis: {
                automargin: true,
                tickangle: -45,
            },
            yaxis: {
                title: 'Values',
                automargin: true
            },
            legend: { orientation: "h", y: -0.2 }
        };

        var config = { responsive: true };

        Plotly.newPlot('bar_chart', traces, layout, config);
    }

    // initial render on DOMContentLoaded
    document.addEventListener('DOMContentLoaded', function () {
        try {
            var data = window.AI_CHART_DATA || {};
            renderChart(data);
        } catch (err) {
            console.error("ai_chart.js error:", err);
        }
    });

    // expose a reload function to update chart dynamically from other scripts
    window.aiAma = window.aiAma || {};
    window.aiAma.reloadChart = function (newChartData) {
        try {
            // if newChartData is a string, try to parse
            var parsed = (typeof newChartData === 'string') ? JSON.parse(newChartData) : newChartData;
            renderChart(parsed);
        } catch (e) {
            console.error("aiAma.reloadChart error:", e);
        }
    };
})();
