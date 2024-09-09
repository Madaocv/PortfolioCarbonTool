document.addEventListener("DOMContentLoaded", function() {
    var root = am5.Root.new("chartdiv");

    root.setThemes([am5themes_Animated.new(root)]);

    var container = root.container.children.push(am5.Container.new(root, {
        layout: root.verticalLayout,
        width: am5.percent(100),
        height: am5.percent(100)
    }));

    var title = container.children.push(am5.Label.new(root, {
        text: "Main Chart Graph",
        fontSize: 25,
        fontWeight: "bold",
        textAlign: "center",
        x: am5.p50,
        centerX: am5.p50,
        paddingBottom: 10
    }));

    var chartContainer = container.children.push(am5.Container.new(root, {
        layout: root.horizontalLayout,
        width: am5.percent(100),
        height: am5.percent(100)
    }));

    var leftTitle = chartContainer.children.push(am5.Label.new(root, {
        text: "Left Title",
        fontSize: 15,
        fontWeight: "bold",
        rotation: -90,
        textAlign: "center",
        y: am5.p50,
        centerY: am5.p50,
        paddingRight: 10
    }));

    var bottomTitle = container.children.push(am5.Label.new(root, {
        text: "Bottom title",
        fontSize: 15,
        fontWeight: "bold",
        textAlign: "center",
        x: am5.p50,
        centerX: am5.p50,
        paddingTop: 10
    }));

    var chart = chartContainer.children.push(am5xy.XYChart.new(root, {
        panX: true,
        panY: true,
        wheelY: "zoomXY",
        pinchZoomX: true,
        pinchZoomY: true
    }));

    var xAxis = chart.xAxes.push(am5xy.ValueAxis.new(root, {
        renderer: am5xy.AxisRendererX.new(root, {
            minGridDistance: 50,
            stroke: am5.color(0x000000),
            strokeWidth: 2,
        }),
        tooltip: am5.Tooltip.new(root, {}),
    }));

    var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
        renderer: am5xy.AxisRendererY.new(root, {
            minGridDistance: 50,
            stroke: am5.color(0x000000),
            strokeWidth: 2,
        }),
        tooltip: am5.Tooltip.new(root, {}),
    }));

    var series0 = chart.series.push(am5xy.LineSeries.new(root, {
        calculateAggregates: true,
        xAxis: xAxis,
        yAxis: yAxis,
        valueYField: "y",
        valueXField: "x",
        valueField: "value",
        tooltip: am5.Tooltip.new(root, {
            labelText: "{text}\nx: {valueX}, y: {valueY}"
        })
    }));

    var circleTemplate = am5.Template.new({});
    series0.bullets.push(function() {
        var graphics = am5.Circle.new(root, {
            radius: 5,
            fill: series0.get("fill"),
            tooltipText: "{text}\nx: {valueX}, y: {valueY}" 
        }, circleTemplate);

        return am5.Bullet.new(root, {
            sprite: graphics
        });
    });

    series0.set("heatRules", []);
    series0.strokes.template.set("strokeOpacity", 0);

    xAxis.on("start", updateAxisPosition);
    xAxis.on("end", updateAxisPosition);
    yAxis.on("start", updateAxisPosition);
    yAxis.on("end", updateAxisPosition);
    chart.yAxesAndPlotContainer.events.on("positionchanged", updateAxisPosition);
    chart.plotContainer.events.on("boundschanged", updateAxisPosition);

    function updateAxisPosition() {
        var plotWidth = chart.plotContainer.width();
        var plotHeight = chart.plotContainer.height();

        var x = xAxis.get("renderer").positionToCoordinate(xAxis.valueToPosition(0)) - plotWidth;
        if (x > 0) {
            x = 0;
        }
        if (x < -plotWidth) {
            x = -plotWidth;
        }
        yAxis.set("x", x);

        var y = yAxis.get("renderer").positionToCoordinate(yAxis.valueToPosition(0)) - plotHeight;
        if (y > 0) {
            y = 0;
        }
        if (y < -plotHeight) {
            y = -plotHeight;
        }
    }

    // Глобальні змінні для індикатора і анімації
    var indicator, hourglass, hourglassanimation;

    // Функція для створення індикатора завантаження
    function createIndicator() {
        if (!indicator) {
            indicator = root.container.children.push(am5.Container.new(root, {
                width: am5.p100,
                height: am5.p100,
                layer: 1000,
                background: am5.Rectangle.new(root, {
                    fill: am5.color(0xffffff),
                    fillOpacity: 0.7
                })
            }));

            indicator.children.push(am5.Label.new(root, {
                text: "Loading...",
                fontSize: 25,
                x: am5.p50,
                y: am5.p50,
                centerX: am5.p50,
                centerY: am5.p50
            }));

            hourglass = indicator.children.push(am5.Graphics.new(root, {
                width: 32,
                height: 32,
                fill: am5.color(0x000000),
                x: am5.p50,
                y: am5.p50,
                centerX: am5.p50,
                centerY: am5.p50,
                dy: -45,
                svgPath: "M12 5v10l9 9-9 9v10h24V33l-9-9 9-9V5H12zm20 29v5H16v-5l8-8 8 8zm-8-12-8-8V9h16v5l-8 8z"
            }));

            hourglassanimation = hourglass.animate({
                key: "rotation",
                to: 180,
                loops: Infinity,
                duration: 2000,
                easing: am5.ease.inOut(am5.ease.cubic)
            });
        }
    }

    // Показати індикатор
    function showIndicator() {
        createIndicator(); // Переконайтеся, що індикатор створено
        hourglassanimation.play();
        indicator.show();
    }

    // Приховати індикатор
    function hideIndicator() {
        hourglassanimation.pause();
        indicator.hide();
    }

    // Fetch initial data for the chart
    fetchDataAndUpdateChart();

    document.getElementById("selectPortfolio").addEventListener("change", fetchDataAndUpdateChart);
    document.getElementById("selectReference").addEventListener("change", fetchDataAndUpdateChart);
    document.getElementById("absoluteRelativeSwitch").addEventListener("change", fetchDataAndUpdateChart);
    document.getElementById("companyContributionSwitch").addEventListener("change", fetchDataAndUpdateChart);

    function fetchDataAndUpdateChart() {
        var portfolio = document.getElementById("selectPortfolio").value;
        var reference = document.getElementById("selectReference").value;
        var absoluteRelative = document.getElementById("absoluteRelativeSwitch").checked;
        var companyContribution = document.getElementById("companyContributionSwitch").checked;

        // Show the loading indicator
        showIndicator();

        var data = {
            portfolio: portfolio,
            reference: reference,
            absoluteRelative: absoluteRelative,
            companyContribution: companyContribution
        };

        fetch("/api/calculate-chart-data/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    // Тут кидаємо помилку, щоб обробити її в catch
                    throw new Error(data.error || "Something went wrong");
                });
            }
            return response.json();
        })
        .then(data => {
            if (!data.error) {
                updateChart(data);
                hideIndicator(); // Приховуємо індикатор завантаження
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error.message);  // Відображаємо повідомлення про помилку в консолі

            // Відображаємо повідомлення про помилку
            const dangerAlert = document.getElementById('danger-alert');
            dangerAlert.innerText = error.message; // Використовуємо повідомлення з помилки
            dangerAlert.style.visibility = 'visible'; // Робимо повідомлення видимим
            // Приховуємо повідомлення через 10 секунд
            setTimeout(() => {
                dangerAlert.style.visibility = 'hidden';
            }, 10000); // 10000 мс = 10 секунд
            // hideIndicator(); // Приховуємо індикатор завантаження навіть у разі помилки
        });
    }

    function updateChart(data) {
        series0.data.setAll(data.data);

        title.set("text", data.maintitle);
        leftTitle.set("text", data.lefttitle);
        bottomTitle.set("text", data.bottomtitle);
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    updateAxisPosition();
});
