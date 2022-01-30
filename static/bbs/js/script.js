window.addEventListener("load" , function (){ 

    $("#submit").on("click", function(){ ajax_send(); });

});

function delete_comment(identifier){

    $.ajax({
        url: identifier + "/",
        type: "DELETE",
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 
        $("#comment_area").html(data.content);
    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    });

}

function ajax_send(){

    let form_elem   = "#form_area";
    let data        = new FormData( $(form_elem).get(0) );
    let url         = $(form_elem).prop("action");
    let method      = $(form_elem).prop("method");

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 
        //Done
        $("#comment_area").html(data.content);
    }).fail( function(xhr, status, error) {
        //Fail
        console.log(status + ":" + error );
    }); 
    

}
