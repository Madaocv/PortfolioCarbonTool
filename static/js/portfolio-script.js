document.addEventListener('DOMContentLoaded', function() {
  // Ініціалізація Sortable.js
  var sortable = new Sortable(document.getElementById('sortable-portfolios'), {
      animation: 150,
      onEnd: function(evt) {
          submitForm(); // Виклик submitForm після перетягування
      }
  });

  // Викликаємо submitForm при завантаженні сторінки
  submitForm();

  // Додаємо обробник подій для кожного чекбоксу
  document.querySelectorAll('input[name="portfolios"]').forEach((checkbox) => {
      checkbox.addEventListener('change', function() {
          console.log('Checkbox changed:', checkbox.value, 'Checked:', checkbox.checked); // Лог для перевірки
          submitForm(); // Виклик submitForm при зміні стану чекбоксу
      });
  });
});

function submitForm() {
  console.log('submitForm called');
  const selectedPortfolios = [];
  let anyChecked = false;

  // Використовуємо простіший селектор для вибору чекбоксів
  document.querySelectorAll('input[name="portfolios"]').forEach((checkbox, index) => {
      console.log('Checkbox found:', checkbox); // Лог для перевірки, чи знайдено чекбокс
      console.log('Checkbox:', checkbox.value, 'Checked:', checkbox.checked);

      if (checkbox.checked) {
          anyChecked = true;
      }
      selectedPortfolios.push({
          id: checkbox.value,
          checked: checkbox.checked,
          order: index + 1
      });
  });

  if (!anyChecked) {
      console.log('No checkboxes selected. Current state of selectedPortfolios:', selectedPortfolios);
      document.getElementById('danger-alert').style.visibility = 'visible';
      return;
  } else {
      console.log('At least one checkbox selected');
      document.getElementById('danger-alert').style.visibility = 'hidden';
  }

  console.log('Selected portfolios:', selectedPortfolios);

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
      console.log('Data received:', data);

      // Побудова графіків на основі отриманих даних
      const mockData1 = [
        { x: 'A', y: 2 },
        { x: 'B', y: 1 },
        { x: 'C', y: 3 },
        { x: 'D', y: 2.5 }
    ];
  
    const mockData2 = [
        { x: 'A', y: 4 },
        { x: 'B', y: 2.5 },
        { x: 'C', y: 5 },
        { x: 'D', y: 3.5 }
    ];
  
    // Використовуємо замокані дані для побудови графіків
    buildChart1(mockData1);
    buildChart2(mockData2);
  })
  .catch((error) => {
      console.error("Error:", error);
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

// Статична функція побудови графіків
function buildChart1(chartData) {
    // chart 1
    const root1 = am5.Root.new("chartdiv1");
    const chart1 = root1.container.children.push(
        am5xy.XYChart.new(root1, {})
    );

    const xAxis1 = chart1.xAxes.push(am5xy.CategoryAxis.new(root1, {
        renderer: am5xy.AxisRendererX.new(root1, {}),
        categoryField: "x"
    }));
    xAxis1.data.setAll(chartData);

    const yAxis1 = chart1.yAxes.push(am5xy.ValueAxis.new(root1, {
        renderer: am5xy.AxisRendererY.new(root1, {})
    }));

    const series1 = chart1.series.push(
        am5xy.LineSeries.new(root1, {
            xAxis: xAxis1,
            yAxis: yAxis1,
            valueYField: "y",
            categoryXField: "x",
        })
    );

    series1.data.setAll(chartData);
}

function buildChart2(chartData) {
    // chart 2
    const root2 = am5.Root.new("chartdiv2");
    const chart2 = root2.container.children.push(
        am5xy.XYChart.new(root2, {})
    );

    const xAxis2 = chart2.xAxes.push(am5xy.CategoryAxis.new(root2, {
        renderer: am5xy.AxisRendererX.new(root2, {}),
        categoryField: "x"
    }));
    xAxis2.data.setAll(chartData);

    const yAxis2 = chart2.yAxes.push(am5xy.ValueAxis.new(root2, {
        renderer: am5xy.AxisRendererY.new(root2, {})
    }));

    const series2 = chart2.series.push(
        am5xy.ColumnSeries.new(root2, {
            xAxis: xAxis2,
            yAxis: yAxis2,
            valueYField: "y",
            categoryXField: "x",
        })
    );

    series2.data.setAll(chartData);
}
