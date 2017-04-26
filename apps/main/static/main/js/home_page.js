$ (document).ready(function(){
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

  $('#account-dropdown-button').dropdown({
      inDuration: 100,
      outDuration: 100,
      constrainWidth: false, // Does not change width of dropdown to that of the activator
      hover: false, // Activate on hover
      gutter: 14, // Spacing from edge
      belowOrigin: true, // Displays dropdown below the button
      alignment: 'left', // Displays dropdown with edge aligned to the left of button
      stopPropagation: false // Stops event propagation
    }
  );
  $('#new-button').dropdown({
      inDuration: 100,
      outDuration: 100,
      constrainWidth: false, // Does not change width of dropdown to that of the activator
      hover: false, // Activate on hover
      gutter: 14, // Spacing from edge
      belowOrigin: true, // Displays dropdown below the button
      alignment: 'left', // Displays dropdown with edge aligned to the left of button
      stopPropagation: false // Stops event propagation
    }
  );

  $('#file-input').on('change', function(){
    console.log("triggered file input on change")
    $('#file-upload-form').submit();
  })
  $('#file-upload-button').on('click', function(){
    // event.preventDefault()
    console.log("Clicked file upload button")
    $('#file-input').trigger('click');

  })




  $('#account-dropdown.dropdown-content').on('click', function(){
    event.stopPropagation();
  })
  // $('#account-dropdown').on('mouseover', function(){
  //   console.log("hovering over dropdown")
  //   event.stopPropagation();
  // })
  $('#sign-out-button').on('click', function(){
    post_data = {}
    post_data['csrfmiddlewaretoken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value
    $.post({
      url:$(this).attr('href'),
      dataType:'json',
      data:post_data,
      success:function(res){
        console.log(res)
        if (res.redirect !== undefined && res.redirect){
          window.location.href = res.redirect_url
        }
      }
    })
  })





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



var lastSelectedRow;
var trs = $('#main-table tr')


    $('tr').on('click', function(){
        RowClick($(this),false,trs)

    })
})

var lastSelectedRow;
var trs = $('#main-table tr')
// disable text selection
document.onselectstart = function() {
    return false;
}

function RowClick(currenttr, lock, rows) {
    if (window.event.ctrlKey) {
        toggleRow(currenttr);
    }

    if (window.event.button === 0) {

        if (!window.event.ctrlKey && !window.event.shiftKey) {
            clearAll(rows);
            toggleRow(currenttr);
        }

        if (window.event.shiftKey) {
            selectRowsBetweenIndexes([lastSelectedRow.index(), currenttr.index()], rows)
        }
    }
}

function toggleRow(row) {
    if (!row.hasClass('header-row')){
        if (row.hasClass('selected')){
            row.removeClass('selected')
        }
        else{
            row.addClass('selected')

        }
        lastSelectedRow = row;
        }

}

function selectRowsBetweenIndexes(indexes,rows) {
    indexes.sort(function(a, b) {
        return a - b;
    });

    for (var i = indexes[0]; i <= indexes[1]; i++) {
        console.log(rows[i+1])
        $(rows[i+1]).addClass('selected');
    }
}

function clearAll(rows) {
    for (var i = 0; i < rows.length; i++) {
        $(rows[i]).removeClass("selected");
    }
}









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
