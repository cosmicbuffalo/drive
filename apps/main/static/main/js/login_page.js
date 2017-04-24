$(document).ready(function(){

  $('#next-button').on('click', function(){

    //prevent submit
    event.preventDefault();
    //clear message area
    $('#messages-area').html("")


    console.log("*****************************")
    next_button = $(this)
    console.log("triggered ajax function on...")
    console.log(next_button)
    console.log("*****************************")

    post_data = $('#login-form').serialize()
    console.log(post_data)

    $.post({
      url:next_button.attr('ajax-target'),
      data: post_data,
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
            for (var index in res.messages){
              htmlString += "<div class='error-message'>"
              htmlString += res.messages[index]
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
          console.log("Changed Identifier display to res.identifier")
          $('.toggle-transparent').removeClass("transparent")
          console.log("Removed transparent class on identifier display")
          $('.slide-out').hide("slide", {direction:"left"}, 100)

          $('.slide-in').delay(200).show("slide", {direction:"right"}, 100, function(){
              console.log("Slide toggled in second form elements")
          }).delay(1000)
          console.log("Slide toggled hidden form elements")

        }


      }
  })
  })


  $('#sign-in-button').on('click', function(){

    event.preventDefault();
    $('#messages-area').html("")




  })










})
