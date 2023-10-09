"use strict";

$(window).on("load", function(){
    /*
    var recipe_id = window.location.href
    console.log(recipe_id.split('/')[4])

    
    
    $.ajax({
        type: "POST",
        url: "/get_recipe_video",
        data: recipe_id.split('/')[4],
        contentType: "application/json",
        dataType: 'text',
        success: function(result){
            console.log(result);
            $("#recipe_video").attr("src", result)
        } 
    });
    */

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

})
