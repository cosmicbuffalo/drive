$(document).ready(function(){

  $('#next-button').on('click', function(){

    event.preventDefault();


    console.log("*****************************")
    next_button = $(this)
    console.log("triggered ajax function on...")
    console.log(next_button)
    console.log("*****************************")
    $.ajax({
      url:next_button.attr('ajax-target'),
      success: function(res){
        console.log("*****************************")
        console.log("entered success function")
        console.log("res = ")
        console.log(res)

        if (res.result == 'failed_validation'){
          console.log("res.result is equal to failed validation")
          if ('messages' in res){
            console.log("messages in res: ")
            console.log(res.messages)
            htmlString = ""
            for (var message in messages){
              htmlString += "<div class='error-message'>"
              htmlString += messages
              htmlString += "</div>"
            }
            console.log(htmlString)
            $('#messages-area').html(htmlString)
          }
        }
        else{
          console.log("res.result is not equal to failed_validation")
          console.log(res.result)
          console.log("res result ^ should be equal to success!")
          console.log("attempting to retrieve res.identifier....")
          console.log(res.identifier)

          $('#identifier-display').html(res.identifier)
          $('.toggle-transparent').removeClass(transparent)
          $('.toggle-hidden').toggle("slide", {direction:"left"}, 1000)
        }


      }
  })
  })













})
