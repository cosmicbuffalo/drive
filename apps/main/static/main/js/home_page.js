$ (document).ready(function(){

//row selection methods...
    $(".file-flash").click(function() {
        var selected = $(this).hasClass("selected");
        $(".file-flash").removeClass("selected");
        if(!selected)
            $(this).addClass("selected");
    });

    $('.file-flash a').on('click', function(){
        var selected = $(this).hasClass("selected");
        $(".file-flash").removeClass("selected");
        if(!selected)
            $(this).addClass("selected");
    })






  //file upload AJAX
  // $('#file-upload-button').on('click',function(){
  //
  //     event.preventDefault()
  //     $.ajax({
  //         url: $('#file-upload-form').attr('action'),
  //         method: 'post',
  //         data: data,
  //         cache: false,
  //         processData: false,
  //         contentType: false,
  //         success: function(response){
  //             console.log("Entered success function, Response is ...")
  //             console.log(response)
  //
  //             htmlString = ""
  //             htmlString += "<tr class='file-flash'><td>"
  //             htmlString += response.file_data
  //             htmlString += "</td><td>"
  //             htmlString += response.owner_name
  //             htmlString +="</td><td>"
  //             htmlString += response.updated_at
  //             htmlString +="</td><td>"
  //             htmlString += response.file_size
  //             htmlString +="</td></tr>"
  //
  //             $('#table-body').append(htmlString)
  //         }
  //     })
  // })



  //tool bar button functionality
  $('.tool-bar-link').on('click', function(){

    event.preventDefault()

    console.log($('.selected'))

    // $.post({
    //   url:$(this).attr('href'),
    //   data:JSON.stringify($('.selected'))
    //
    //
    // })






  })







})
