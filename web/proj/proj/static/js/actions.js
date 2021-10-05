function send_ajax(target, action) {
    console.log("> actions.js called")

    const card_id = "#card-" + target
    $( card_id ).animate( { height: 0, opacity: 0 , margin: 0}, 1000, "swing", $( this ).remove())

    const csrftoken = getCookie('csrftoken');

    // console.log(action == 'delete_outgoing')

    if(action == 'delete_outgoing') {
        url = "/asyncDeleteOutgoing/"
    } else if(action == 'delete_incoming'){
        url = "/asyncDeleteIncoming/"
    } else if(action == "accept_incoming"){
        url = "/asyncAcceptIncoming/"
    } else if(action == "delete_friend"){
        url = "/asyncDeleteFriend/"
    } else if(action == "send_subscribe_request"){
        url = "/asyncSubscribeRequest/"
    } else if(action == "delete_profile"){
        url = "/profileDelete/"
    } else if(action == "confirm_moderation"){
        url = "/confirmModeration/"
    } else if(action == "dicard_moderation"){
        url = "/discardModeration/"
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

function deleteProfile(){
    var r = confirm("Delete profile?");
    if (r == true) {
      console.log("confirmed");
      send_ajax(0, "delete_profile")
    } else {
      console.log("canceled")
    }

}
