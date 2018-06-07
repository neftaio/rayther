$('#cform').on('valid', function(e) {
  e.preventDefault();
  $.ajax({
    url: '/enviarmensaje',
    data: $('form').serialize(),
    type: 'POST',
    success: function(response) {
      if(response === '{"html": "1"}') {
        // if correct response then show affirmative message
        $('#form-cu-container').html(
          "<div class='row'><div class='mean_title2 cf-title'>Tu Mensaje Ha Sido Enviado Exitosamente</div></div>"
        )
      }
    },
    error: function(error) {
      console.log(error);
    }
  });
});
