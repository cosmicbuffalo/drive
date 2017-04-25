$(document).ready(function(){

  $('#next-step-button').on('click', function(){

    event.preventDefault()

    $('.messages-area').html("")


    post_data = $("#registration-form").serialize()
    console.log("Post data from form: ...")
    console.log(post_data)

    $.post({
      url:$('#next-step-button').attr('ajax-target'),
      data:post_data,
      success: function(res){
        console.log("*****************************")
        console.log("entered success function")
        console.log("res = ")
        console.log(res)

        if (res.result == 'failed_validation'){
          // console.log("res.result is equal to failed validation")
          if ('messages' in res){
            // console.log("messages in res: ")
            console.log(res.messages)

            if (res.messages.name_errors.length > 0){
              htmlString = ""
              for (var index in res.messages.name_errors){
                htmlString += "<div class='error-message'>"
                htmlString += res.messages.name_errors[index]
                htmlString += "</div>"
              }
              $('#name-error-div').html(htmlString)
            }
            if (res.messages.email_errors.length > 0){
              htmlString = ""
              for (var index in res.messages.email_errors){
                htmlString += "<div class='error-message'>"
                htmlString += res.messages.email_errors[index]
                htmlString += "</div>"
              }
              $('#email-error-div').html(htmlString)
            }
            if (res.messages.password_errors.length > 0){
              htmlString = ""
              for (var index in res.messages.password_errors){
                htmlString += "<div class='error-message'>"
                htmlString += res.messages.password_errors[index]
                htmlString += "</div>"
              }
              $('#password-error-div').html(htmlString)
            }
            if (res.messages.password_confirm_errors.length > 0){
              htmlString = ""
              for (var index in res.messages.password_confirm_errors){
                htmlString += "<div class='error-message'>"
                htmlString += res.messages.password_confirm_errors[index]
                htmlString += "</div>"
              }
              $('#password-confirm-error-div').html(htmlString)
            }
            if (res.messages.birthday_errors.length > 0){
              htmlString = ""
              for (var index in res.messages.birthday_errors){
                htmlString += "<div class='error-message'>"
                htmlString += res.messages.birthday_errors[index]
                htmlString += "</div>"
              }
              $('#birthday-error-div').html(htmlString)
            }
            if (res.messages.gender_errors.length > 0){
              htmlString = ""
              for (var index in res.messages.gender_errors){
                htmlString += "<div class='error-message'>"
                htmlString += res.messages.gender_errors[index]
                htmlString += "</div>"
              }
              $('#gender-error-div').html(htmlString)
            }
            if (res.messages.phone_errors.length > 0){
              htmlString = ""
              for (var index in res.messages.phone_errors){
                htmlString += "<div class='error-message'>"
                htmlString += res.messages.phone_errors[index]
                htmlString += "</div>"
              }
              $('#phone-error-div').html(htmlString)
            }
            if (res.messages.location_errors.length > 0){
              htmlString = ""
              for (var index in res.messages.location_errors){
                htmlString += "<div class='error-message'>"
                htmlString += res.messages.location_errors[index]
                htmlString += "</div>"
              }
              $('#location-error-div').html(htmlString)
            }
          }
        }
        else{

          console.log(res.validated_data)
          console.log(JSON.stringify(res.validated_data))

          post_data = res.validated_data
          console.log("***********************************")
          console.log("Attempting to retrieve csrfmiddlewaretoken...")
          console.log(document.getElementsByName('csrfmiddlewaretoken')[0].value)
          post_data['csrfmiddlewaretoken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value
          console.log("post_data is ...")
          console.log(post_data)

          $.post({
            url:$('#registration-form').attr('action'),
            data:post_data,
            dataType: "json",
            success: function(res){
              console.log("*****************************")
              console.log("entered success function")
              console.log("res = ")
              console.log(res)

              if (res.redirect !== undefined && res.redirect) {
                window.location.href = res.redirect_url;
              }



            }
          })


          // console.log("About to submit form")
          // $('#registration-form').submit()

        }

      }
    })



  })









})
