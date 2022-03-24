/*
$(document).ready(function() {

$(".btn").click(function(){
    $.ajax({
        url: '/user_input/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            key: 'hello'
        },
        success: function(response) {
            console.log(response);
            alert("Ok!");
        }
    });
});
});
    */
