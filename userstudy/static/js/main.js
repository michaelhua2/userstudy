$(document).ready(function() {
/*
    var teaser = document.getElementsByClassName("teaser");

    if( teaser.length > 0 ) {
        setInterval('cycleImages()', 2000);
    }
  */
  $('#crossfade').cycle({
    speed: 500,
    timeout: 2000,
    caption: "#adv-custom-caption",
    captionTemplate: "{{cycleTitle}}",
  }); 

  $('#reason-row:hidden:first');


  $('.trial-select').popover('show');
  $('.trial-hover').popover("show");
  //$('.trial-next').popover("show");
  $('.trial-reason').popover("show");
  $('.trial-next-formal').popover("show");
});

function show_reason_trial(){
    $("#reason-row").fadeIn( "slow" );
    $("#show-reason-btn").hide();
    $("#trial-next-btn").show();

    $('.trial-reason').popover("show");
    $('.trial-next').popover("hide");
    $('.trial-next-formal').popover("show");
}

function show_reason() {
    
    /*$('#reason-row').tab('show');*/

    $("#reason-row").fadeIn( "slow" );

    $("#show-reason-btn").hide();
    $("#next-btn").show();

}


function show_waiting(){
    $('#myPleaseWait').modal('show');
}


function hover_image(img) {
    document.getElementById("display-img").src = img.src;
    document.getElementById("display-caption").innerHTML = "Magnify: " + img.name;
}

function select_image(input_block){

    var img_block_all = document.getElementsByClassName("img-block");
    var input_img = input_block.getElementsByClassName("compare-img")[0];
    
    for(i = 0; i < img_block_all.length; i++) {
        var img     = img_block_all[i].getElementsByClassName("compare-img")[0];
        var caption = img_block_all[i].getElementsByClassName("img-caption")[0];
        var vote    = img_block_all[i].getElementsByClassName("img-vote")[0];

        if( $("#" + img.id).hasClass("voted") ) {

            $("#" + img.id).removeClass("voted");
            $("#" + caption.id).removeClass("voted-text");
            $("#" + caption.id).text("Method " + (i+1).toString());
            $("#" + vote.id).val("0");
        }

        if( img.name == input_img.name ) {

            $("#" + img.id).addClass("voted");
            $("#" + caption.id).addClass("voted-text");
            $("#" + caption.id).text("Method " + (i+1).toString() + " (selected)");
            $("#" + vote.id).val("1");
        }
        
    }

}


function check_next(input) {
    
    if( input.getAttribute("class") == "img-block" ) {
        select_image(input);
    }

    var num_voted = $(".voted").length;
    if( num_voted > 0 ) {
        $('#next-btn').removeAttr('disabled');
    } else {
        $('#next-btn').attr('disabled', true);
    }

}

function check_vote() {
    /*
    var vote1 = $("#img1-vote").val();
    var vote1 = $("#img2-vote").val();

    if( vote1 == 0 && vote2 == 0 ) {
        alert("Please select ");
    }*/
    document.getElementById('main_form').submit();

}


function validate_info() {
    
    var gender  = $("#gender-selector").val();
    var age     = $("#age-selector").val();
    var exp     = $("#exp-selector").val();
    
    if( gender + age + exp > 3 ) {
        $('#info-next-btn').removeAttr('disabled');
    }

}