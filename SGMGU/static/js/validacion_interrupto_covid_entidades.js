/**
 * Created by Daniel.
 */

$(document).on('ready', function () {

    var municipio = $('#id_municipio'),
        organismo = $('#id_organismo'),
        entidad = $('#id_entidad'),
        municipios_entidades = [];
        municipio.find('option').each(function (k, v) {
            municipios_entidades.push(v);
        });

    function seleccionar_entidades() {

        $.ajax({
            data: {'id_municipio': municipio.val(), 'id_organismo': organismo.val()},
            url: '/peticion_ajax/filtrar_entidades_interruptos_covid/',
            type: 'get',
            success: function (entidades) {
                var html = '';
                html += '<option value="">-------</option>';
                for (var i = 0; i < entidades.length; i++) {
                    html += '<option value=' + entidades[i].codigo_ent + '>' + entidades[i].e_nombre + '</option>';
                }
                entidad.html(html);
            }
        })
    }

    if (organismo.val() !== ''){
         municipio.prop('disabled', false);
    } else{
        municipio.prop('disabled', true);
    }

    organismo.on('change', function(){
        if($(this).val() === ''){
            municipio.prop('disabled', true);
        }else{
            municipio.prop('disabled', false);
        }
    });

    if (municipio.val() !== ''){
         seleccionar_entidades();
    }

    municipio.on('change', function(){

        if($(this).val() === ''){
            entidad.prop('disabled', true);
        }else{
            entidad.prop('disabled', false);

            seleccionar_entidades();
        }
    });


});