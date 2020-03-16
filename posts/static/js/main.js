function createSubscription() {

    $('a.follow').click(function(event){
        var btn = $(this);
        $.ajax(btn.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'pk': btn.data('pk'),
                'action': btn.data('action'),
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
        });
    });
}


$(document).ready(function(){
    createSubscription();
});