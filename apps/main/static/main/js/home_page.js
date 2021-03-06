$(document).ready(function () {

  $(document).on('click', function(){
    $('#right-click-menu-div').slideUp(200);
  })

  //---------------------------
  //------ TOOLBAR STUFF ------
  //---------------------------

  $('#preview-button').on('click', function () {
    console.log("Clicked preview button")
    var rows = $('tr.selected')
    console.log(rows)
    console.log(rows.length)
    if (rows.length == 1) {
      console.log(rows[0])
      img = $('tr.selected :first-child div img')
      console.log(img)
      img.trigger('click')
    }
  })

  $('#share-button').on('click', function () {

    for (var x = 0; x < $('table .selected').length; x += 1){
      console.log($('table .selected')[x].attributes)

      var id = ($('table .selected')[x].attributes[1].value)
      console.log(id)
      var type = ($('table .selected')[x].attributes[2].value)
      console.log(type)
      var htmlString = "<input type='hidden' name='" + type + "' value='" + id + "'>"
      $('#share-items-form').append(htmlString)

    }

    $('#share-items-form').ajaxForm({
      success: function (res) {
        console.log(res)
        alert("Share success!");
        $('#share-modal').modal('close')
        $.get({
          url: "home/folder_body/" + res["folder_id"],
          success: function (result) {
            replaceTableBody(result)
          }
        })
      }
    })


    $('#share-modal').modal();


  })


  $('#move_to_trash').on('click', function () {

    var post_data = {}
    var num_rows = 0
    event.preventDefault()
    for (var i = 0; i < $('table .selected').length; i = i + 1) {
      console.log($('table .selected')[i].attributes)

      var id = ($('table .selected')[i].attributes[1].value)
      var type = ($('table .selected')[i].attributes[2].value)


      post_data[i] = { "type": type, 'id': id, }
      num_rows += 1
    }


    post_data['csrfmiddlewaretoken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value
    post_data["num_rows"] = num_rows
    $.post({
      url: '/move_to_trash',
      data: post_data,
      dataType: 'json',
      success: function (res) {

        $('table .selected').delay(400).slideToggle(400).delay(500)
        $('table .selected').delay(400).remove()

        // console.log(res)
        // $.get({
        //     url: "/folder_body/" + res.current_folder,
        //     success:function(new_html){
        //         replaceTableBody(new_html)
        //         // assignSelectionHandler();
        //     }
        // })
      }


    })

  })



  //-------------------------
  //-----  AJAX MENUS  ------
  //-------------------------


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
    gutter: 0, // Spacing from edge
    belowOrigin: true, // Displays dropdown below the button
    alignment: 'left', // Displays dropdown with edge aligned to the left of button
    stopPropagation: false // Stops event propagation
  }
  );


  $('#file-upload-button').on('click', function () {
    // event.preventDefault()
    console.log("Clicked file upload button")
    $('#file-input').trigger('click');
  })
  assignFileUploadHandler();

  $('#new-folder-button').on('click', function () {
    console.log("clicked new folder tab")

    $('#modal1').modal();
    $('#modal1').modal('open')
    // $('#folder-create-override').trigger('click')
  })


  $('#account-dropdown.dropdown-content').on('click', function () {
    event.stopPropagation();
  })

  $('#sign-out-button').on('click', function () {
    post_data = {}
    post_data['csrfmiddlewaretoken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value
    $.post({
      url: $(this).attr('href'),
      dataType: 'json',
      data: post_data,
      success: function (res) {
        console.log(res)
        if (res.redirect !== undefined && res.redirect) {
          window.location.href = res.redirect_url
        }
      }
    })
  })


  //------------------------------
  //---- NAVIGATION TAB STUFF ----
  //------------------------------


  $('#left-bar-tab-menu li').on('click', function () {

    console.log("clicked left bar tab")
    console.log($(this))
    $('#left-bar-tab-menu li').removeClass('selected')
    $(this).addClass('selected')

  })

  $('#my-drive-tab').on('click', function () {
    console.log("Clicked my drive")
    $.get({
      url: $(this).attr('href'),
      success: function (res) {
        // console.log(res)
        $('#breadcrumb-div').html('<a class="breadcrumb first-crumb" href="#"><span class="crumb-hover">My Drive</span></a>')
        replaceTableBody(res)

      }
    })
  })
  $('#trash-tab').on('click', function () {
    $.get({
      url: $(this).attr('href'),
      success: function (res) {
        replaceTableBody(res)
      }
    })
  })
  $('#shared-tab').on('click', function () {
    $.get({
      url: $(this).attr('href'),
      success: function (res) {
        replaceTableBody(res)
      }
    })
  })
  $('#recent-tab').on('click', function () {
    $.get({
      url: $(this).attr('href'),
      success: function (res) {
        replaceTableBody(res)
      }
    })
  })


  //---------------------------
  //------ ROW SELECTION ------
  //---------------------------


  var lastSelectedRow;
  $('#table-body').on('click', 'tr.item-row', function () {
    var rows = $('#tbody-content-table tr')
    console.log("triggered row selection handler")
    RowClick($(this), false, rows)
    $('#selection-tools').css('display', 'inline-block')
    var selected = $('tr.selected')
    if (selected.length == 1) {
      // console.log("There is one row selected")
      selected_type = $(selected[0])[0].attributes['item-type'].value
      // console.log(selected_type)
      if (selected_type != "folder") {
        $('#preview-button').css('display', 'inline-block')
      } else {
        $('#preview-button').css('display', 'none')
      }
    } else {
      // console.log("there are... " + String(selected.length) + " rows selected")
      $('#preview-button').css('display', 'none')
    }
  })
  //-----------------------------
  //----TILED VIEW SELECTION-----
  //-----------------------------
  var lastSelectedRow;
  $('#table-body').on('click', 'div.tile', function () {
    var tiles = $('.tile')
    console.log("triggered row selection handler")
    RowClick($(this), false, tiles)
    $('#selection-tools').css('display', 'inline-block')
    var selected = $('div.tile.selected')
    if (selected.length == 1) {
      // console.log("There is one row selected")
      // $(selected).css('background-color',"#5764f7")
      selected_type = $(selected[0])[0].attributes['item-type'].value
      // console.log(selected_type)
      if (selected_type != "folder") {
        $('#preview-button').css('display', 'inline-block')
      } else {
        $('#preview-button').css('display', 'none')
      }
    } else {
      // console.log("there are... " + String(selected.length) + " rows selected")
      $('#preview-button').css('display', 'none')
    }
  })


//-----------------------------
//--------- GRID VIEW ---------
//-----------------------------


  $('#view-change-icon').hover(
    function(){
      if ($(this).attr('src') == $(this).attr('grid-gray')){
        $(this).attr('src', $(this).attr('grid-black'))
      } else if ($(this).attr('src') == $(this).attr('list-grey')) {
        $(this).attr('src', $(this).attr('list-black'))
      }

    },
    function(){
      if ($(this).attr('src') == $(this).attr('grid-black')){
        $(this).attr('src', $(this).attr('grid-gray'))
      } else if ($(this).attr('src') == $(this).attr('list-black')){
        $(this).attr('src', $(this).attr('list-grey'))
      }
    }
  )

  $("#view-change-icon").on('click', function () {
    $('.header-row').toggle()
    var current
    if ($("#table-body").css("background-color") == "rgb(255, 255, 255)" ){
      current = "grid"
      $("#table-body").css({"background-color": "rgb(245, 245, 245)"})
      $('#tbody-content-wrapper').css({'border-left':'none'})
      console.log("if working")
    }
    else{
      current ="table"
      $("#table-body").css({"background-color":"rgb(255, 255, 255)"})
      console.log("else working")
      $('#tbody-content-wrapper').css({'border-left':'1px solid #ebebeb'})
    }
    if ($(this).attr("src") == $(this).attr("list-black")){
      $(this).attr("src", $(this).attr('grid-black'))
    } else if ($(this).attr("src") == $(this).attr("grid-black")){
      $(this).attr('src', $(this).attr('list-black'))
    }

    $.get({
      url: $(this).attr('href'),
      success: function (res) {
        $('#tbody-content-wrapper').delay(400).remove()
        $.get({
          url: "home/folder_body/" + res["current_folder"],
          success: function (result) {
            replaceTableBody(result)
            if (current == "grid"){
               $('#tbody-content-wrapper').css({'border-left':'none'})
            }


          }
        })
      }
    })
  })

  //---------------------------
  //---- FOLDER NAVIGATION ----
  //---------------------------

  // $('#breadcrumb-div').on('click', 'a#first-crumb', function(){
  //   event.preventDefault()
  //   event.stopPropagation()
  //   $('#my-drive-tab').trigger('click')
  // })


  $('#breadcrumb-div').on('click', 'a.not-first', function () {
    event.preventDefault()
    console.log("You just clicked a breadcrumb")
    console.log($(this).attr('href'))
    console.log($(this))
    var clicked = $(this)

    $.get({
      url: $(this).attr('href'),
      success: function (res) {
        replaceTableBody(res)
        console.log(clicked)
        console.log(clicked.nextAll('a.breadcrumb'))
        clicked.nextAll('a.breadcrumb').remove()
      }
    })

  })

  $('#breadcrumb-div').on('click', '#first-crumb', function () {
    console.log("clicked first child")
    event.preventDefault()
    console.log($(this))
    // $(this).stop()
    $('#my-drive-tab').trigger('click')
  })

  $('#breadcrumb-div').on('mouseover', '.breadcrumb:last-child', function(){
    console.log("hovering over last breadcrumb")
    $('.breadcrumb:last-child').attr('data-activates', 'new-button-dropdown')
    $('.breadcrumb:last-child').addClass('dropdown-button')

    $('.breadcrumb:last-child').dropdown({
      inDuration: 100,
      outDuration: 100,
      constrainWidth: false, // Does not change width of dropdown to that of the activator
      hover: false, // Activate on hover
      gutter: 29, // Spacing from edge
      belowOrigin: true, // Displays dropdown below the button
      alignment: 'left', // Displays dropdown with edge aligned to the left of button
      stopPropagation: true // Stops event propagation
    }
    );
    return
    $('.breadcrumb:last-child').dropdown('open')
  })


  $('#table-body').on('click', '.folder-name-div a', function () {
    console.log("You just clicked a folder link!")
    event.preventDefault()
    var folder_name = $(this)[0].innerText
    // console.log(folder_name)
    href = $(this).attr('href')
    // console.log(href)

    $.get({
      url: $(this).attr('href'),
      success: function (res) {
        replaceTableBody(res)
        $('#breadcrumb-div').append('<a class="breadcrumb not-first" href=' + href + '><span class="crumb-hover">' + folder_name + '</span></a>')
      }
    })
  })

  //Initialize first view of root folder
  $.get({
    url: $('#my-drive-tab').attr('href'),
    success: function (res) {
      // console.log(res)
      replaceTableBody(res)
      $('#breadcrumb-div').html('<a id="first-crumb" class="breadcrumb" href="#"><span class="crumb-hover">My Drive</span></a>')
    }
  })

  //--------------------------
  //----- BEAUTIFICATION -----
  //--------------------------

  $(document).on('contextmenu', function(e){
    e.preventDefault()
  })

  $('#table-body').on('contextmenu', ' tbody tr', function(e){
    console.log($(this))
    console.log($(this)[0])
    console.log($($(this)[0]).attr('item-type'))
    console.log($($(this)[0]).attr('item-id'))

    var post_data = {}

    if ($(this).hasClass('selected')){
      console.log("right clicked selection")
      post_data['selection'] = true;
      var selected = $('tr.selected')
      console.log(selected)
      post_data['num_selected'] = selected.length
      for (var x = 0; x < selected.length; x+=1){
        console.log(selected[x])
        post_data[String(x)] = $(selected[x]).attr('item-type') + ':' + $(selected[x]).attr('item-id')
      }
      console.log(post_data)
    } else{
      console.log("clicked outside selection")
      post_data['selection'] = false;
      post_data['num_selected'] = 1
      post_data['0'] = $($(this)[0]).attr('item-type') + ':' + $($(this)[0]).attr('item-id')
      console.log(post_data)
      var rows = $('#tbody-content-table tr')
      clearAll(rows)
      toggleRow($(this))
    }

    post_data['csrfmiddlewaretoken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value

    $.post({
      url:$('#right-click-menu-div').attr('href'),
      data:post_data,
      success:function(res){
        console.log(res)
        $('#right-click-menu-div').html(res)
        $('#right-click-menu-div').css('top', determineMouseY(e) + 'px')
        $('#right-click-menu-div').css('left', mouseX(e) + 'px')
        $('#right-click-menu-div').slideDown(300, function(){

        })
      }
    })

    e.preventDefault()
  });



})//END OF DOCUMENT.READY FUNCTION




//----------------------------
//----- HELPER FUCNTIONS -----
//----------------------------



// disable text selection
document.onselectstart = function () {
  return false;
}

function RowClick(currenttr, lock, rows) {
  if (window.event.ctrlKey || window.event.metaKey) {
    toggleRow(currenttr);
  }

  if (window.event.button === 0) {

    if (!window.event.ctrlKey && !window.event.shiftKey && !window.event.metaKey) {
      clearAll(rows);
      toggleRow(currenttr);
    }

    if (window.event.shiftKey) {
      selectRowsBetweenIndexes([lastSelectedRow.index(), currenttr.index()], rows)
    }
  }
}

function toggleRow(row) {
  if (!row.hasClass('header-row')) {
    if (row.hasClass('selected')) {
      row.removeClass('selected')
      // console.log(rows)
    }
    else {
      row.addClass('selected')
    }
    lastSelectedRow = row;
  }

}

function selectRowsBetweenIndexes(indexes, rows) {
  indexes.sort(function (a, b) {
    return a - b;
  });

  for (var i = indexes[0]; i <= indexes[1]; i++) {
    $(rows[i]).addClass('selected');
  }
}

function clearAll(rows) {
  for (var i = 0; i < rows.length; i++) {
    $(rows[i]).removeClass("selected");
  }
}

function replaceTableBody(new_html) {
  console.log("replacing html...")
  $('#selection-tools').fadeOut(300)
  $('#table-body').fadeOut(300, function () {
    $('#table-body').html(new_html)
    $('#table-body').delay(100).fadeIn(300, function () {
      console.log('done')
      $('.materialboxed').materialbox();
      assignFileUploadHandler()
      $('#file-upload-form').ajaxForm({
        success: function (res) {
          console.log(res)
          alert("File Upload Success!");
          $.get({
            url: "home/folder_body/" + res["folder_id"],
            success: function (result) {
              replaceTableBody(result)
            }
          })
        }
      })
      $('#folder-create-form').ajaxForm({
        success: function (res) {
          console.log(res)
          alert("Folder Creation Success!");
          $('#modal1').modal('close')
          $.get({
            url: "home/folder_body/" + res["folder_id"],
            success: function (result) {
              replaceTableBody(result)
            }
          })
        }
      })
    })
  })
}

function assignFileUploadHandler() {
  $('#file-input').on('change', function () {
    console.log("triggered file input on change")
    $('#file-upload-form').submit();
  })

}

// $(document).bind("click", function() {
//     document.getElementById("right-click-menu").remove();
// });



function mouseX(evt) {
if (evt.pageX) {
    return evt.pageX;
} else if (evt.clientX) {
   return evt.clientX + (document.documentElement.scrollLeft ?
       document.documentElement.scrollLeft :
       document.body.scrollLeft);
} else {
    return null;
}
}

function mouseY(evt) {
if (evt.pageY) {
    return evt.pageY;
} else if (evt.clientY) {
   return evt.clientY + (document.documentElement.scrollTop ?
   document.documentElement.scrollTop :
   document.body.scrollTop);
} else {
    return null;
}
}


function determineMouseY(evt){
  var window_height = $(window).height()

  var click_mouse_y = mouseY(evt)
  // var menu_height = 397 //Measured in inspector... probably should calculate this

  var menu_height = $('#right-click-menu-div').height()
  console.log(menu_height)

  if (window_height - click_mouse_y < menu_height){
    return window_height - menu_height
  } else {
    return click_mouse_y
  }
}
