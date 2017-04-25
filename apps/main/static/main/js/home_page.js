$ (document).ready(function(){
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



















    // $('#file-upload-button').on('click',function(){
        
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

    //             htmlString = ""
    //             htmlString += "<tr class='file-flash'>"
    //             htmlString += "<td>"
    //             htmlString += response.file_data
    //             htmlString += "</td>"
    //             htmlString += "<td>"
    //             htmlString += response.owner_name
    //             htmlString +="</td>"
    //             htmlString += "<td>"
    //             htmlString += response.updated_at
    //             htmlString +="</td>"
    //             htmlString +="<td>"
    //             htmlString += response.file_size
    //             htmlString +="</td></tr>"


    //             $('#table-body').append(htmlString)



    //         }


    //     })




    // })









