document.addEventListener('DOMContentLoaded', function() {
    var sortable = new Sortable(document.getElementById('sortable-portfolios'), {
        animation: 150,
        ghostClass: 'sortable-ghost', // Клас, що застосовується до елемента під час перетягування
        onEnd: function(evt) {
            saveOrderAndState();
        }
    });

    function saveOrderAndState() {
        const order = [];
        document.querySelectorAll('#sortable-portfolios .form-check').forEach((checkElement, index) => {
            const checkbox = checkElement.querySelector('input[type="checkbox"]');
            order.push({
                id: checkbox.value,
                checked: checkbox.checked,
                order: index
            });
        });

        // Відправляємо на сервер через fetch
        fetch('/save-portfolio-order/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ portfolios: order })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Order and state saved:', data);
        })
        .catch(error => {
            console.error('Error saving order and state:', error);
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
});
