let root1, root2; // глобальні змінні для збереження кореневих елементів
let loadingIndicator1, loadingIndicator2, loadingAnimation1, loadingAnimation2;
let loadingRoot1, loadingRoot2;
document.addEventListener('DOMContentLoaded', function() {
  console.log('*'.repeat(10));
  // Ініціалізація Sortable.js
  var sortable = new Sortable(document.getElementById('sortable-portfolios'), {
      animation: 50,
      onEnd: function(evt) {
          updateColors();
          submitForm(); // Виклик submitForm після перетягування
      }
  });

  // Викликаємо submitForm при завантаженні сторінки
  submitForm();

  // Додаємо обробник подій для кожного чекбоксу
  document.querySelectorAll('input[name="portfolios"]').forEach((checkbox) => {
      checkbox.addEventListener('change', function() {
          // console.log('Checkbox changed:', checkbox.value, 'Checked:', checkbox.checked); // Лог для перевірки
          updateColors();
          submitForm(); // Виклик submitForm при зміні стану чекбоксу
      });
  });
});
  // Функція оновлення кольорів і тексту
  function updateColors() {
    const selectedCheckboxes = Array.from(document.querySelectorAll('input[name="portfolios"]:checked'));
    const portfolioItems = document.querySelectorAll('#sortable-portfolios .flex'); // Клас для всіх sortable об'єктів

    // Спочатку скидаємо всі стилі
    portfolioItems.forEach(item => {
      item.classList.remove('bg-blue-300', 'bg-red-300', 'hover:bg-blue-200', 'hover:bg-red-200'); // Видаляємо кольори
      const label = item.querySelector('label');
    //   label.innerText = item.getAttribute('data-original-text'); // Скидаємо текст до початкового
    });

    if (selectedCheckboxes.length === 1) {
      // Якщо вибрано тільки один чекбокс, робимо об'єкт синім
      const selectedItem = selectedCheckboxes[0].closest('.flex');
    //   selectedItem.classList.add('bg-blue-300');
      selectedItem.classList.add('bg-blue-300', 'hover:bg-blue-200');
    } else if (selectedCheckboxes.length > 1) {
      // Якщо вибрано більше одного об'єкта
      selectedCheckboxes.forEach((checkbox, index) => {
        const item = checkbox.closest('.flex');
        const label = item.querySelector('label');
        if (index === selectedCheckboxes.length - 1) {
          // Останній об'єкт стає червоним і до тексту додається "Reference"
        //   item.classList.add('bg-red-300');
          item.classList.add('bg-red-300', 'hover:bg-red-200');
        //   label.innerText = label.innerText + " (Reference)";
        } else {
          // Інші об'єкти стають синіми
          item.classList.add('bg-blue-300', 'hover:bg-blue-200');
        }
      });
    }
  }
function submitForm() {
  // console.log('submitForm called');
    // Спочатку видаляємо старі графіки, якщо вони є
    if (root1) root1.dispose();
    if (root2) root2.dispose();

    // Показуємо індикатори завантаження
    showLoadingIndicator1();
    showLoadingIndicator2();
  const selectedPortfolios = [];
  let anyChecked = false;

  // Використовуємо простіший селектор для вибору чекбоксів
  document.querySelectorAll('input[name="portfolios"]').forEach((checkbox, index) => {
      // console.log('Checkbox found:', checkbox); // Лог для перевірки, чи знайдено чекбокс
      // console.log('Checkbox:', checkbox.value, 'Checked:', checkbox.checked);

      if (checkbox.checked) {
          anyChecked = true;
      }
      selectedPortfolios.push({
          id: checkbox.value,
          checked: checkbox.checked,
          order: index + 1
      });
  });
  // console.log('Selected portfolios:', selectedPortfolios);
  const checkedCount = selectedPortfolios.filter(item => item.checked).length;
  if (checkedCount < 2) {
    //   console.log('No checkboxes selected. Current state of selectedPortfolios:', selectedPortfolios);
    // console.log('Less than two checkboxes selected. Current state of selectedPortfolios:', selectedPortfolios);  
    document.getElementById('danger-info').style.visibility = 'visible';
    hideLoadingIndicator1();
    hideLoadingIndicator2();
      return;
  } else {
      // console.log('At least two checkbox selected');
      document.getElementById('danger-info').style.visibility = 'hidden';
  }

  // console.log('Selected portfolios:', selectedPortfolios);
  // console.log('Where is animation ?');
//   showLoadingIndicator1();
//   showLoadingIndicator2();
  // Відправка даних на сервер
  fetch("/api/calculate-portfolio-data/", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ portfolios: selectedPortfolios }),
  })
  .then(response => response.json())
  .then(data => {
      // console.log('Data received:', data);
        // Приховуємо індикатори, коли дані отримані
        hideLoadingIndicator1();
        hideLoadingIndicator2();
      if (data.chart1.render === true) {

        // Очищаємо старі графіки
        if (root1) root1.dispose();

        root1 = buildWaterfallChart("chartdiv1", data.chart1.data, data.chart1.serieslen);
      }
      if (data.chart2.render === true) {
        // console.log("This is render chart 2 true");
        // Очищаємо старі графіки
        if (root2) root2.dispose();
        // console.log(data.chart2.data);
        root2 = buildChart2("chartdiv2", data.chart2.data, {
            maintitle: 'Main',
            lefttitle: data.chart2.lefttitle,
            bottomtitle: data.chart2.bottomtitle
        });
      }

  })
  .catch((error) => {
      console.error("Error:", error);
              // Приховуємо індикатори, коли дані отримані
              hideLoadingIndicator1();
              hideLoadingIndicator2();
  });
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

function buildChart2(div, chartData, chartTitles) {
    // Очищаємо контейнер для графіка
    cleanChartContainer(div);

    root2 = am5.Root.new(div); // Локальна змінна root

    root2.setThemes([am5themes_Animated.new(root2)]); // Додаємо тему

    // Контейнер для графіка
    var container = root2.container.children.push(am5.Container.new(root2, {
        layout: root2.verticalLayout,
        width: am5.percent(100),
        height: am5.percent(100)
    }));

    // Додаємо основний заголовок
    // var title = container.children.push(am5.Label.new(root2, {
    //     text: chartTitles.maintitle || '',
    //     fontSize: 25,
    //     fontWeight: "bold",
    //     textAlign: "center",
    //     x: am5.p50,
    //     centerX: am5.p50,
    //     paddingBottom: 10
    // }));

    var chartContainer = container.children.push(am5.Container.new(root2, {
        layout: root2.horizontalLayout,
        width: am5.percent(100),
        height: am5.percent(100)
    }));

    // Додаємо заголовок для лівої осі
    var leftTitle = chartContainer.children.push(am5.Label.new(root2, {
        text: chartTitles.lefttitle || '',
        fontSize: 15,
        fontWeight: "bold",
        rotation: -90,
        textAlign: "center",
        y: am5.p50,
        centerY: am5.p50,
        paddingRight: 10
    }));

    // Додаємо заголовок для нижньої осі
    var bottomTitle = container.children.push(am5.Label.new(root2, {
        text: chartTitles.bottomtitle || '',
        fontSize: 15,
        fontWeight: "bold",
        textAlign: "center",
        x: am5.p50,
        centerX: am5.p50,
        paddingTop: 10
    }));

    // Створюємо XY-графік
    const chart = chartContainer.children.push(am5xy.XYChart.new(root2, {
        panX: true,
        panY: true,
        wheelY: "zoomXY",
        pinchZoomX: true,
        pinchZoomY: true
    }));

    // Налаштування осі X
    const xAxis = chart.xAxes.push(am5xy.ValueAxis.new(root2, {
        renderer: am5xy.AxisRendererX.new(root2, {
            minGridDistance: 50,
            stroke: am5.color(0x000000),
            strokeWidth: 2
        }),
        tooltip: am5.Tooltip.new(root2, {})
    }));
    // Додаємо адаптер для підписів осі X, щоб додати знак %
    xAxis.get("renderer").labels.template.adapters.add("text", function(text) {
        return text + "%";
    });
    // Налаштування осі Y
    const yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root2, {
        renderer: am5xy.AxisRendererY.new(root2, {
            minGridDistance: 50,
            stroke: am5.color(0x000000),
            strokeWidth: 2
        }),
        tooltip: am5.Tooltip.new(root2, {})
    }));

    // Створюємо серію для даних
    const series = chart.series.push(
        am5xy.LineSeries.new(root2, {
            xAxis: xAxis,
            yAxis: yAxis,
            valueYField: "y",
            valueXField: "x",
            tooltip: am5.Tooltip.new(root2, {
                labelText: "{text}\nx: {valueX}, y: {valueY}"
            })
        })
    );

    // Додаємо дані в серію
    series.data.setAll(chartData);

    // Налаштовуємо кола для точок на графіку
    var circleTemplate = am5.Template.new({});
    series.bullets.push(function() {
        var graphics = am5.Circle.new(root2, {
            radius: 10,
            fill: series.get("fill"),
            tooltipText: "{text}\nx: {valueX}, y: {valueY}"
        }, circleTemplate);

        return am5.Bullet.new(root2, {
            sprite: graphics
        });
    });

    // Приховуємо лінії між точками
    series.strokes.template.setAll({
        strokeWidth: 2,
        strokeOpacity: 0
    });

    // Відображення шкали осі X у центрі графіка
    function updateAxisPosition() {
        var plotHeight = chart.plotContainer.height();
        var y = yAxis.get("renderer").positionToCoordinate(yAxis.valueToPosition(0)) - plotHeight;
        if (y > 0) {
            y = 0;
        }
        if (y < -plotHeight) {
            y = -plotHeight;
        }
        xAxis.set("y", y);  // Встановлюємо вісь X в центрі
    }

    // Оновлення позицій осей при змінах
    xAxis.on("start", updateAxisPosition);
    xAxis.on("end", updateAxisPosition);
    yAxis.on("start", updateAxisPosition);
    yAxis.on("end", updateAxisPosition);
    chart.yAxesAndPlotContainer.events.on("positionchanged", updateAxisPosition);
    chart.plotContainer.events.on("boundschanged", updateAxisPosition);

    // Повертаємо root для подальшого очищення
    return root2;
}

// Функція очищення контейнера
function cleanChartContainer(id) {
  let chartContainer = document.getElementById(id);
  if (chartContainer) {
    chartContainer.innerHTML = ''; // Очищаємо вміст контейнера
  }
}
function buildWaterfallChart(divId, chartData, numOfSeries) {
    // Очищаємо контейнер для графіка
    am5.array.each(am5.registry.rootElements, function(root) {
      if (root.dom.id === divId) {
        root.dispose();
      }
    });
  
    // Створюємо root елемент
    var root = am5.Root.new(divId);
  
    // Додаємо тему
    root.setThemes([am5themes_Animated.new(root)]);
  
    // Створюємо графік
    var chart = root.container.children.push(
      am5xy.XYChart.new(root, {
        panX: false,
        panY: false,
        wheelX: "panX",
        wheelY: "zoomY",
        pinchZoomY: true // Додаємо можливість збільшення по Y
      })
    );
  
    // Додаємо повзунок для осі Y
    chart.set("scrollbarY", am5.Scrollbar.new(root, {
      orientation: "vertical"
    }));
  
    // Створюємо осі
    var xAxis = chart.xAxes.push(
      am5xy.CategoryAxis.new(root, {
        maxDeviation: 0.3,
        categoryField: "category",
        renderer: am5xy.AxisRendererX.new(root, {
          minGridDistance: 30,
          strokeOpacity: 0.1
        }),
        tooltip: am5.Tooltip.new(root, {})
      })
    );
  
    // Додаємо обмеження для тексту категорій на осі X
    xAxis.get("renderer").labels.template.setAll({
      maxWidth: 100,  // Максимальна ширина тексту
      oversizedBehavior: "wrap",  // Текст буде переноситися на новий рядок
      textAlign: "center",  // Текст буде центруватися
    //   rotation: -45,  // Додаємо поворот тексту для кращого вигляду
      centerY: am5.p50,  // Центруємо текст по осі Y
      centerX: am5.p50   // Центруємо текст по осі X
    });
  
    var yAxis = chart.yAxes.push(
      am5xy.ValueAxis.new(root, {
        maxDeviation: 0.3,
        renderer: am5xy.AxisRendererY.new(root, {
          strokeOpacity: 0.1
        })
      })
    );
  
    // Додаємо дані в осі
    xAxis.data.setAll(chartData);
  
    // Задаємо кольори для серій (синій і зелений)
    const colorPalette = [
      am5.color(0x3498db), // Синій
      am5.color(0x2ecc71), // Зелений
      am5.color(0xe74c3c), // Червоний
      am5.color(0xf1c40f), // Жовтий
      am5.color(0x9b59b6)  // Фіолетовий
    ];
  
    // Створюємо серії для кожної пари open/close
    function createSeries(openField, closeField, name, colorIndex) {
      var series = chart.series.push(
        am5xy.ColumnSeries.new(root, {
          name: name,
          xAxis: xAxis,
          yAxis: yAxis,
          valueYField: closeField,
          openValueYField: openField,
          categoryXField: "category",
          clustered: false,
          fill: colorPalette[colorIndex % colorPalette.length], // Використовуємо кольори з палітри
          stroke: colorPalette[colorIndex % colorPalette.length] // Задаємо колір для меж колонок
        })
      );
  
      // Додаємо підписи до серій
      series.bullets.push(function() {
        return am5.Bullet.new(root, {
          sprite: am5.Label.new(root, {
            text: "{valueY}",
            centerY: am5.p50,
            centerX: am5.p50,
            populateText: true,
            fill: am5.color(0xffffff),
            // Обмеження розміру тексту, щоб уникнути перекриття
            maxWidth: 60,  // Задаємо максимальну ширину для тексту
            wrap: true,    // Додаємо перенесення тексту
            fontSize: 12   // Зменшуємо розмір шрифту для кращого вигляду
          })
        });
      });
  
      // Додаємо анімацію на графік
      series.appear(1000);
      series.data.setAll(chartData);
    }
  
    // Генеруємо серії на основі кількості пар open/close
    for (let i = 1; i <= numOfSeries; i++) {
      createSeries(`open${i}`, `close${i}`, `Series ${i}`, i - 1); // Використовуємо кольори з палітри
    }
  
    // Анімація при завантаженні графіку
    chart.appear(1000, 100);
    
    return root;
}


// Глобальні змінні для індикаторів завантаження
function showLoadingIndicator1() {
    // Видаляємо root для графіка перед показом індикатора
    if (root1) root1.dispose();

    // Якщо індикатор вже є, не створюємо новий
    if (!loadingRoot1) {
        loadingRoot1 = am5.Root.new("chartdiv1"); // Створюємо окремий root для індикатора
        let indicator = loadingRoot1.container.children.push(am5.Container.new(loadingRoot1, {
            width: am5.p100,
            height: am5.p100,
            layer: 1000,
            background: am5.Rectangle.new(loadingRoot1, {
                fill: am5.color(0xffffff),
                fillOpacity: 0.7
            })
        }));

        indicator.children.push(am5.Label.new(loadingRoot1, {
            text: "Loading...",
            fontSize: 25,
            x: am5.p50,
            y: am5.p50,
            centerX: am5.p50,
            centerY: am5.p50
        }));

        // Додаємо SVG-годинник
        let hourglass = indicator.children.push(am5.Graphics.new(loadingRoot1, {
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

        // Додаємо анімацію обертання
        hourglass.animate({
            key: "rotation",
            to: 360,
            loops: Infinity,
            duration: 2000,
            easing: am5.ease.inOut(am5.ease.cubic)
        });
    }
}

function hideLoadingIndicator1() {
    if (loadingRoot1) {
        loadingRoot1.dispose(); // Звільняємо root після завершення
        loadingRoot1 = null; // Очищаємо змінну
    }
}

function showLoadingIndicator2() {
    // Видаляємо root для графіка перед показом індикатора
    if (root2) root2.dispose();

    // Якщо індикатор вже є, не створюємо новий
    if (!loadingRoot2) {
        loadingRoot2 = am5.Root.new("chartdiv2"); // Створюємо окремий root для індикатора
        let indicator = loadingRoot2.container.children.push(am5.Container.new(loadingRoot2, {
            width: am5.p100,
            height: am5.p100,
            layer: 1000,
            background: am5.Rectangle.new(loadingRoot2, {
                fill: am5.color(0xffffff),
                fillOpacity: 0.7
            })
        }));

        indicator.children.push(am5.Label.new(loadingRoot2, {
            text: "Loading...",
            fontSize: 25,
            x: am5.p50,
            y: am5.p50,
            centerX: am5.p50,
            centerY: am5.p50
        }));

        // Додаємо SVG-годинник
        let hourglass = indicator.children.push(am5.Graphics.new(loadingRoot2, {
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

        // Додаємо анімацію обертання
        hourglass.animate({
            key: "rotation",
            to: 360,
            loops: Infinity,
            duration: 2000,
            easing: am5.ease.inOut(am5.ease.cubic)
        });
    }
}

function hideLoadingIndicator2() {
    if (loadingRoot2) {
        loadingRoot2.dispose(); // Звільняємо root після завершення
        loadingRoot2 = null; // Очищаємо змінну
    }
}
