$(document).ready(function(){

  $('#next-step-button').on('click', function(){

    event.preventDefault()

    $('.messages-area').html("")


    post_data = $("#registration-form").serialize()
    console.log("Post data from form: ...")
    console.log(post_data)



  })









})
