/**
 * Created by Daniel.
 */

$(document).on('ready', function () {

    var nivel_escolar = $('#id_nivel_escolar');

        if (nivel_escolar.val() !== ''){
            var carrera = $('#id_carrera'),
                id_nivel_escolar = nivel_escolar.val();

            if (id_nivel_escolar == 5 || id_nivel_escolar == 6){

                carrera.prop('disabled', false);
                carrera.prop('required', true);

                $.ajax({
                data: {'id_nivel_escolar': id_nivel_escolar},
                url: '/peticion_ajax/seleccionar_carreras/',
                type: 'get',
                success: function (carreras) {
                    var html = '';
                    html += '<option value="">-------</option>';

                    for (var i = 0; i < carreras.length; i++) {
                        html += '<option value="' + carreras[i].id_carrera + '" >' +
                            carreras[i].nombre_carrera + '</option>';
                     }

                    carrera.html(html);
                }
            })

            }else{
                carrera.prop('disabled', true);
                carrera.prop('required', false);
            }
        }

        nivel_escolar.on('change', function () {
            var carrera = $('#id_carrera'),
                id_nivel_escolar = nivel_escolar.val();

            if (id_nivel_escolar == 5 || id_nivel_escolar == 6){

                carrera.prop('disabled', false);
                carrera.prop('required', true);

                $.ajax({
                data: {'id_nivel_escolar': id_nivel_escolar},
                url: '/peticion_ajax/seleccionar_carreras/',
                type: 'get',
                success: function (carreras) {
                    var html = '';
                    html += '<option value="">-------</option>';

                    for (var i = 0; i < carreras.length; i++) {
                        html += '<option value="' + carreras[i].id_carrera + '">' +
                            carreras[i].nombre_carrera + '</option>';
                     }

                    carrera.html(html);
                }
            })

            }else{
                carrera.prop('disabled', true);
                carrera.prop('required', false);
            }

        });

});