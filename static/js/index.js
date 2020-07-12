function findPosts() {
    let block = document.getElementById('SimpleList');
    let results = block.querySelectorAll("[id^=elem_]");

    let ids = [];
    let regexp = /elem_(\d+)/;

    results.forEach(function(item) {
        let elem = item.id;
        ids.push(Number(elem.match(regexp)[1]));
    })
    console.log("IDs:s", ids);
    return ids;
}

function findCheckboxes() {
    let block = document.getElementById('SimpleList');
    let results = block.querySelectorAll("[id^=cbox_]");
    console.log(results);

    let ids = [];
    let regexp = /cbox_(\d+)/;

    results.forEach(function(item) {
        if (item.checked) {
            let elem = item.id;
            ids.push(Number(elem.match(regexp)[1]));
        }
    })
    console.log("Deleting IDs:s", ids);
    return ids
}

submitingButton = document.getElementById('submiting_btn');
deletingButton = document.getElementById('deleting_btn');

submitingButton.onclick = function(e) {
    e.preventDefault();
    console.log("ajax-submit is working!") // debug
    $.ajax({
        url : "/", // endpoint
        type : "POST",
        data : { posts: findPosts(),
                 action: "submit",
                 csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                 }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            if (json.result != 'Success') {
                $('#results').html("<div class='alert-box radius' data-alert>An error occured while handeling your request"+
                 "<a href='#' class='close'>&times;</a></div>"); }
            else {
                $('#results').html("<div class='alert-box alert radius' data-alert>Data has been sent"+
                "<a href='#' class='close'>&times;</a></div>"); }
            console.log(json); // log the returned json to the console
            console.log("success"); // another debug check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>We have encountered an error: "+errmsg+
            "<p>This operation is undoable</p>"+"<a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // more info about the error
        }
    });
};

deletingButton.onclick = findCheckboxes

//deletingButton.onclick = function(e) {
//    e.preventDefault();
//    console.log("ajax-delete is working!") // debug
//    $.ajax({
//        url : "/", // endpoint
//        type : "POST",
//        data : { posts: findElems(),
//                 action: "delete",
//                 csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
//                 }, // data sent with the post request
//
//        // handle a successful response
//        success : function(json) {
//            if (json.result != 'Success') {
//                $('#results').html("<div class='alert-box radius' data-alert>An error occured while handeling your request"+
//                 "<a href='#' class='close'>&times;</a></div>"); }
//            else {
//                $('#results').html("<div class='alert-box alert radius' data-alert>Data has been sent"+
//                "<a href='#' class='close'>&times;</a></div>"); }
//            console.log(data);
//            console.log(json); // log the returned json to the console
//            console.log("success"); // another debug check
//        },
//
//        // handle a non-successful response
//        error : function(xhr,errmsg,err) {
//            $('#results').html("<div class='alert-box alert radius' data-alert>We have encountered an error: "+errmsg+
//            "<p>This operation is undoable"+" <a href='#' class='close'>&times;</a></div>"); // add error to the dom
//            console.log(xhr.status + ": " + xhr.responseText); // more info about the error
//        }
//    });
//};