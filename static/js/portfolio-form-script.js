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
            console.log('Checkbox changed:', checkbox.value, 'Checked:', checkbox.checked); // Додаємо лог для перевірки
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
    })
    .catch((error) => {
        console.error("Error:", error);
    })
    .finally(() => {
        // Приховуємо індикатор завантаження
        hideIndicator();
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

// Приховати індикатор
function hideIndicator() {
    hourglassanimation.pause();
    indicator.hide();
}