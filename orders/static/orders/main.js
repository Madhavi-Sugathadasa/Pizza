var csrfcookie = function() {
    var cookieValue = null,
        name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.status_change').forEach(select => {
        select.onchange = () => {
            const selected_option = select.value;
            const order_id = select.dataset.order;

            // Initialize new request
            const request = new XMLHttpRequest();
            request.open('POST', '/' + order_id + '/change_status');
            request.setRequestHeader("X-CSRFToken", csrfcookie());

            request.onload = () => {

                // Extract JSON data from request
                const data = JSON.parse(request.responseText);

                // Update the result div
                if (data.success) {
                    console.log("order status updated")
                } else {
                    console.log("Error updating order status")
                }
            }

            // Add data to send with request
            const data = new FormData();
            data.append('status', selected_option);

            // Send request
            request.send(data);
            return false;
        };
    });


});
