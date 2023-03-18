$(document).ready(function (event) {

  var api_domain = "http://127.0.0.1:8000";

  // window.location("/OTP/index.html");
  
  $("#signup_proceed_btn").click(function (event) {
    
    event.preventDefault();

    var fdata = {
      "user_type": $("#user_type").val(),
      "fname": $("#fname").val(),
      "lname": $("#lname").val(),
      "phone": $("#phone").val(),
      "gender": $("#gender").val(),
      "email": $("#email").val(),
      "password": $("#password1").val()
    }

    $.ajax({
      url: `${api_domain}/account/register`,
      type: "POST",
      data: fdata,

      success: function (result) {
        console.log("Result :: " + result.message.text);
        
        $("#myModal").show();
        setTimeout(() => {
          $("#myModal").hide();
          window.location = "registraion-success";
        }, 3000);

        // setTimeout(() => {

        //   // localStorage.setItem("userData", null);
        //   // localStorage.setItem("userData", result.data);
        
        //   window.location = "/";

        // }, 3000);



      }
    });

  });



  $("#login_proceed_btn").click(function (event) {
    
    event.preventDefault();

    var fdata = {
      "email": $("#email").val(),
      "password": $("#password").val()
    }

    $.ajax({
      url: `${api_domain}/account/login`,
      type: "POST",
      data: fdata,

      success: function (result) {
        console.log("Result :: " + result.message.text);
        
        $("#myModal").show();
        setTimeout(() => {
          $("#myModal").hide();
          window.location = "/";
        }, 3000);


      }
    });

  });


  $("#forgot_password_proceed_btn").click(function (event) {
    
    event.preventDefault();

    var fdata = {
      "email": $("#email").val(),
    }

    $.ajax({
      url: `${api_domain}/account/forgot-password`,
      type: "POST",
      data: fdata,

      success: function (result) {
        console.log("Result :: " + result.message.text);
        
        $("#myModal").show();
        setTimeout(() => {
          $("#myModal").hide();
          window.location = "forgot-password-success";
        }, 3000);


      }
    });

  });




  $('#emailHelp').hide();
  $('#passwordHelp').hide();
  $('#conPasswordHelp').hide();


  // Error msg Start
  $('#proceed').click(function() {
    var sEmail = $('#email').val();
    if ($.trim(sEmail).length == 0) {
      $('#emailHelp').show();
      e.preventDefault();
    }
    if (validateEmail(sEmail)) {
      $('#emailHelp').hide();
    } else {
      $('#emailHelp').show();
      e.preventDefault();
    }
  });

  $('#proceed').click(function(event) {
      if ($('#pass').val().length == 0) { //if pass field is empty
          $('#passwordHelp').show();
          preventDefault(event);
    }
    if ($('#pass').val().length) { //if pass has value
      $('#passwordHelp').hide();
      $('#proceed').click(function(){
        window.location("/OTP/index.html");
      });
    }

  });

  $('#proceed').click(function(event) {
      if ($('#confirm-pass').val().length == 0) { //if pass field is empty
          $('#conPasswordHelp').show();
          preventDefault(event);
    }
    if ($('#comfirm-pass').val().length) { //if pass has value
      $('#conPasswordHelp').hide();
      $('#proceed').click(function(){
        window.location("/OTP/index.html");
      });
    }

  });

  function validateEmail(sEmail) {
    var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
    if (filter.test(sEmail)) {
      return true;
    } else {
      return false;
    }
  }


});