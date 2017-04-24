$ (document).ready(function(){
    $(".file-flash").click(function() {
        var selected = $(this).hasClass("highlight");
        $(".file-flash").removeClass("highlight");
        if(!selected)
            $(this).addClass("highlight");
    });

    $('#file-upload-button').on('click',function(){
        event.preventDefault()
        $.ajax({
            url: $('#file-upload-form').attr('action'),
            method: 'post',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(response){
                console.log("Entered success function, Response is ...")
                console.log(response)

                htmlString = ""
                htmlString += "<tr class='file-flash'>"
                htmlString += "<td>"
                htmlString += response.file_data
                htmlString += "</td>"
                htmlString += "<td>"
                htmlString += response.owner_name
                htmlString +="</td>"
                htmlString += "<td>"
                htmlString += response.updated_at
                htmlString +="</td>"
                htmlString +="<td>"
                htmlString += response.file_size
                htmlString +="</td></tr>"


                $('#table-body').append(htmlString)



            }


        })




    })







})

