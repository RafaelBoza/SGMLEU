/**
 * Created by MRiguera on 16/11/2017.
 */


$(document).on('ready', function () {

    // $("#gestion-demanda").on("submit", ".js-demanda-create-form", function () {
    //     console.log("entro al $(#gestion-demanda)");
    //     var form = $(this);
    //     $.ajax({
    //         url: form.attr("action"),
    //         data: form.serialize(),
    //         type: form.attr("method"),
    //         dataType: 'json',
    //         success: function () {
    //             if (data.form_is_valid) {
    //                 alert("La demanda se ha creado");
    //             } else {
    //                 $("#gestion-demanda .modal-content").html(data.html_form);
    //             }
    //         }
    //     });
    //     return false;
    // });

    $(".js-create-demanda").click(function () {
        $("#gestion-demanda").on("submit", ".js-demanda-create-form", function () {
            var form = $(this);
            $.ajax({
                url: form.attr("action"),
                data: form.serialize(),
                type: form.attr("method"),
                dataType: 'json',
                success: function (data) {
                    if (data.form_is_valid) {
                        alert("La demanda ha sido creada");
                    } else {
                        $("#gestion-demanda .modal-content").html(data.html_form);
                    }
                }
            });
            return false;
        });
    });

    // $(".js-create-demanda").click(function () {
    //     $.ajax({
    //         url: '/demandas/demanda_create/',
    //         type: 'get',
    //         dataType: 'json',
    //         beforeSend: function () {
    //             $("#gestion-demanda").modal("show");
    //         },
    //         success: function (data) {
    //             $("#gestion-demanda .modal-content").html(data.html_form);
    //         }
    //     });
    // });



});






