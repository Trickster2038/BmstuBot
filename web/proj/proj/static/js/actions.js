function send_ajax(target, action) {
    console.log("> actions.js called")

    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: "POST",
        url: "http://localhost:8000/asyncview/",
    data: { csrfmiddlewaretoken: csrftoken,   // < here 
        state:"inactive", 
        target: target
    },
    success: function() {
        // alert("pocohuntus")
        console.log("ajax delivered")
    }
})
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
