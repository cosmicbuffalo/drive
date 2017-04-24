$ (document).ready(function(){
    
    $(".file-flash").click(function() {
    var selected = $(this).hasClass("highlight");
    $(".file-flash").removeClass("highlight");
    if(!selected)
            $(this).addClass("highlight");
});
})

