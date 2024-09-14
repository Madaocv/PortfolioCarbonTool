let root1, root2; // глобальні змінні для збереження кореневих елементів

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
          console.log('Checkbox changed:', checkbox.value, 'Checked:', checkbox.checked); // Лог для перевірки
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
          item.classList.add('bg-blue-300');
        }
      });
    }
  }
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

      // Очищаємо старі графіки
      if (root1) root1.dispose();
      if (root2) root2.dispose();

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
      root1 = buildChart("chartdiv1", mockData1);
      root2 = buildChart("chartdiv2", mockData2);
      console.log("Hello world!");
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
function buildChart(div, chartData) {
    // Очищаємо контейнер для графіка
    cleanChartContainer(div);

    let root = am5.Root.new(div); // Локальна змінна root

    const chart = root.container.children.push(
        am5xy.XYChart.new(root, {})
    );

    const xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
        renderer: am5xy.AxisRendererX.new(root, {}),
        categoryField: "x"
    }));
    xAxis.data.setAll(chartData);

    const yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
        renderer: am5xy.AxisRendererY.new(root, {})
    }));

    const series = chart.series.push(
        am5xy.LineSeries.new(root, {
            xAxis: xAxis,
            yAxis: yAxis,
            valueYField: "y",
            categoryXField: "x",
        })
    );

    series.data.setAll(chartData);
    
    return root; // Повертаємо root для подальшого очищення
}

// Функція очищення контейнера
function cleanChartContainer(id) {
  let chartContainer = document.getElementById(id);
  if (chartContainer) {
    chartContainer.innerHTML = ''; // Очищаємо вміст контейнера
  }
}
