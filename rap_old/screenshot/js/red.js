window.redblock = function (search_str){
    var s = search_str;
    $('a').each( function () {
        if($(this).attr("href") == s){
            $(this).css('border','3px solid red');
        }
    });
};

