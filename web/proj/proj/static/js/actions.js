function send_ajax(target, action) {
    console.log("> actions.js called")

    const card_id = "#card-" + target
    $( card_id ).animate( { height: 0, opacity: 0 , margin: 0}, 1000, "swing", $( this ).remove())

    const csrftoken = getCookie('csrftoken');

    // console.log(action == 'delete_outgoing')

    if(action == 'delete_outgoing') {
        url = "http://localhost:8000/asyncDeleteOutgoing/"
    } else if(action == 'delete_incoming'){
        url = "http://localhost:8000/asyncDeleteIncoming/"
    } else if(action == "accept_incoming"){
        url = "http://localhost:8000/asyncAcceptIncoming/"
    } else if(action == "delete_friend"){
        url = "http://localhost:8000/asyncDeleteFriend/"
    } else if(action == "send_subscribe_request"){
        url = "http://localhost:8000/asyncSubscribeRequest/"
    }

    $.ajax({
        type: "POST",
        url: url,
    data: { csrfmiddlewaretoken: csrftoken,   // < here 
        state:"inactive", 
        target: target
    },
    success: function() {
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
