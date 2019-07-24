$( document ).ready(function() {
    $('#textButton').hide();
    $('#showButton').hide();
    $('#loaderField').hide();
});



$("form#bank-form").submit(function(event){
    event.preventDefault();
//  activity = $("#bank-form").serializeObject();
    $('#loaderField').show();
    var bank_name = $('form#bankname').val();
    if(bank_name != ''){
        var form = $('#bank-form')[0];
        var formData = new FormData(form);

        console.log(formData);
        var uploadUrl = $('#bank-form').attr('upload-url');
        // $("body").loading('start');
        submitFormnew(formData,uploadUrl,"bank","activity saved successfully",null);
    } else{
        // warningToast("bank name is mandatory")
    }
    return false;
});

function submitFormnew(formData, serviceUrl, callbackToast, callbackMessage, tableId){
    csrftoken = getCSRFToken();
    // var confirmSlug = window.location.pathname.split('/');
    $.ajax({
        headers: { "X-CSRFToken": csrftoken},
        enctype: 'multipart/form-data',
        // beforeSend: function (xhr) {   //Include the bearer token in header
        //     xhr.setRequestHeader("Authorization", 'Bearer '+ tokenData);
        // },
        data: formData,
        processData: false,
        contentType: false,
        dataType: 'json',
        success: function(data){
            console.log("sucess");
            $('#loaderField').hide();
            $('#showButton').show();
            sessionStorage.setItem("refid", data.refId);
        },
        error: function(){
        // $("body").loading('stop');
            $('#loaderField').hide();
            console.log("error occured while fetching response");
        },
        type: 'POST',
        url:serviceUrl
    });
}

/*function to the CSRF token from the browser  */
function getCSRFToken() {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}


$('#getVal').click(function(){
    var getUrl = $(this).attr('get-url');
    getPdfText(getUrl,successget);
});

/*function to get return Type from GstIn*/
function getPdfText(serviceUrl,callback) {
    $.ajax({
    contentType: 'application/json',
    dataType: 'json',
    // beforeSend: function (xhr) {   //Include the bearer token in header
    // xhr.setRequestHeader("Authorization", 'Bearer '+ tokenData);
    // },
    data:{
        refid: sessionStorage.getItem('refid')
    },
    success: function(data){
        // $("body").loading('stop');
        if(data.status == "SUCCESS"){
            callback(data.data);
        } else{
            // errorToast(data.message);
        }
    },
    error: function(error){
        // $("body").loading('stop');
      // errorToast("error occured while fetching response");
      console.log(error);
    },
    type: 'GET',
    url: serviceUrl
  });
}

function successget(arg) {
    $('#showButton').hide();
    $('#textButton').show();
    $('textarea#pdfdata').val(arg);
}
