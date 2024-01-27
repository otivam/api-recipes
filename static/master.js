"use strict";

$(window).on("load", function(){
    if($("input[name='is-logged-in']").val() == "1"){
        $(".breadcrumb .register, .breadcrumb .login").hide();
        $(".breadcrumb .logout").show();
        $(".breadcrumb .logout").addClass("breadcrumb-item");
    }else if($("input[name='is-logged-in']").val() == "0"){
        $(".breadcrumb .register, .breadcrumb .login").show();
        $(".breadcrumb .logout").hide();
        $(".breadcrumb .logout").removeClass("breadcrumb-item");
    }






    //VIDEO MODAL FUNCTIONALITY
    $("tbody img").each(function(){
        var grandparent = $(this).parent().parent().attr("id");

        $(this).on("click", function(){
            $("#video_modal_" + grandparent).modal("show");
        })
    })

    $(".modal-footer button").each(function(){
        var grandparent = $(this).parent().parent().parent().parent().attr("id").slice(12);

        $(this).on("click", function(){
            $("#video_modal_" + grandparent + " .modal-footer").siblings().find("video").attr("src", $("#video_modal_" + grandparent + " .modal-footer").siblings().find("video").attr("src"));
        })
    })

    //TEXT MODAL FUNCTIONALITY
    $("tbody tr").find("td:eq(1) p").each(function(){
        var grandparent = $(this).parent().parent().attr("id");

        $(this).on("click", function(){
            $("#instructions_modal_" + grandparent).modal("show");
        })
    })


    //DETAILS MODAL FUNCTIONALITY
    $(".recipe-details").each(function(){
        var grandparent = $(this).parent().attr("id");

        $(this).on("click", function(){
            $("#details_modal_" + grandparent).modal("show");
        })
    })

    function clearRegisterInputs(){
        $("p[class^='text-danger validation-register']").hide(); //hide the validations
        $("input[name^='register-']").val(""); //empty the inputs
    }


    $(".register-login .register").on("click", function(){
        clearRegisterInputs();
        $("#register_modal").modal("show");
    })

    $(".register-login .login").on("click", function(){
        $("#login_modal").modal("show");
    })

    //VALIDATIONS 
    $(".text-danger, .register-submit").hide();

    function checkAllValidations_register(){
        var register_validation = [repeat_pass(), pass_length(), pass_strength(), validate_email(), ],
            email_validation = $("input[name='register-email']").val() != "",
            username_validation = $("input[name='register-username']").val() != "" && $(".validation-register-username").is(":hidden");

        if(($.inArray(false, register_validation) === -1) && email_validation && username_validation){
            $(".register-submit").show();
            return true;
        }else{
            $(".register-submit").hide();
            return false;
        }
    }

    function pass_length(){
        var pass = $("input[name='register-pass']").val();

        if(pass != ""){
            if(pass.length < 8){
                $(".validation-register-pass-length").show();
                return false;
            }else{
                $(".validation-register-pass-length").hide();
                return true;
            }
        }else{
            return false;
        }
    }

    function containsUppercase(str) {
        return /[A-Z]/.test(str);
    }

    function containsSpecialCharacter(str) {
        return /[^A-Za-z 0-9]/g.test(str);
    }

    function pass_strength(){
        var pass = $("input[name='register-pass']").val();

        if(pass != ""){
            if(!containsUppercase(pass) || !containsSpecialCharacter(pass)){
                $(".validation-register-pass-strength").show();
                return false;
            }else{
                $(".validation-register-pass-strength").hide();
                return true;
            }
        }else{
            return false;
        }

    }

    $("input[name='register-pass']").on("change", function(){
        pass_length();
        pass_strength();
        repeat_pass();
        checkAllValidations_register();
    })



    function repeat_pass(){
        var pass = $("input[name='register-pass']").val(),
            r_pass = $("input[name='register-repeat-pass']").val();

        if(pass != "" && r_pass != ""){
            if(pass != r_pass){
                $(".validation-register-repeat-pass").show();
                return false
            }else{
                $(".validation-register-repeat-pass").hide();
                return true
            }
        }else{
            return false
        }
    }


    $("input[name='register-repeat-pass']").on("change", function(){
        repeat_pass();
        checkAllValidations_register();
    })
        

    $("input[name='register-username']").on("change", function(){
        var username = $("input[name='register-username']").val();

        $.ajax({
            type: "POST",
            url: "/check-username",
            data: JSON.stringify({"username":username}),
            contentType: "application/json",
            dataType: 'json',
            success: function(result){
                if(result["status"] == '1'){
                    $(".validation-register-username").show();
                }else{
                    $(".validation-register-username").hide();
                }
                checkAllValidations_register();
            },
            error: function(error){
                console.log(error);
            }
        });
    })


    $("input[name='register-email']").on("change", function(){
        checkAllValidations_register();
    })



    var validateEmail = (email) => {
        return email.match(
          /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        );
    };

    function validate_email(){
        var email = $("input[name='register-email']").val();

        if(email != ""){
            if(validateEmail(email)){
                $(".validation-register-email").hide();
                return true;
            }else{
                $(".validation-register-email").show();
                return false;
            }
        }else{
            return false;
        }

    }

    $("input[name='register-email']").on("change", function(){
        validate_email();
    })


    // SHOW SUBMIT BUTTON IF USERNAME AND PASSWORDS ARE FILLED IN
    function checkIfEmpty(){
        var username = $("input[name='login-username']").val(),
            password = $("input[name='login-pass']").val();

        if(username != '' && password != ''){
            $(".login-submit").removeAttr('hidden');
        }else{
            $(".login-submit").attr('hidden', true);
        }
    }

    $("input[name='login-username']").on("change", function(){
        checkIfEmpty();
    })

    $("input[name='login-pass']").on("change", function(){
        checkIfEmpty();
    })

    //REGISTER/LOGIN - IF CLOSE IS CLICKED -> REDIRECT TO HOME PAGE
    $(".successful-registration-close, .welcome-close").on("click", function(){
        document.location.href="/";
    })


    $(".breadcrumb-item.logout").on("click", function(){
        $("#logout_modal").modal("show");
    })


    $(".register-submit").on("click", function(){
        var email = $("input[name='register-email']").val(),
            username = $("input[name='register-username']").val(),
            pass = $("input[name='register-pass']").val();

        $(".register-submit").hide();
        $('<div class="spinner-border spinner-register" style="position:absolute; bottom:-18%;" role="status"><span class="sr-only"></span></div>').insertAfter(".register-submit");
        
        $.ajax({
            type: "POST",
            url: "/register-user",
            data: JSON.stringify({"email":email, "username":username, "pass":pass}),
            contentType: "application/json",
            dataType: 'json',
            success: function(result){
                console.log(result);
                if(result["status"] == '1'){
                    clearRegisterInputs();
                    $("#register_modal").find(".register-close").trigger("click");
                    $("#successful_register_modal").modal("show");
                    $(".spinner-register").hide();
                }
            },
            error: function(error){
                console.log(error);
            }
        });
        
    })

    $(".login-submit").on("click", function(){
        var username = $("input[name='login-username']").val(),
            pass = $("input[name='login-pass']").val();

        $.ajax({
            type: "POST",
            url: "/login",
            data: JSON.stringify({"username":username, "pass":pass}),
            contentType: "application/json",
            dataType: 'json',
            success: function(result){
                console.log(result);
                if(result["status"] == "0"){
                    $(".validation-login").show();
                }else{
                    $(".validation-login").hide();
                    $(".breadcrumb .register, .breadcrumb .login").hide();
                    $(".breadcrumb .logout").show();
                    $(".breadcrumb .logout").addClass("breadcrumb-item");

                    $("#login_modal").find(".login-close").trigger("click");
                    $("#successful_login_modal").modal("show");
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    })

    $(".breadcrumb .logout").on("click", function(){
        $(this).hide();
        $(".breadcrumb .register,.breadcrumb .login").show();
        $(".breadcrumb .logout").removeClass("breadcrumb-item");

        $.ajax({
            type: "POST",
            url: "/logout",
            contentType: "application/json",
            dataType: 'json',
            success: function(result){
                console.log(result);
            },
            error: function(error){
                console.log(error);
            }
        });
    })






})
