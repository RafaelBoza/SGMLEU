/**
 * Created by Daniel.
 */

$(document).on('ready', function () {

    var municipio = $('#id_municipio'),
        entidad = $('#id_entidad'),
        municipios_entidades = [];
        municipio.find('option').each(function (k, v) {
            municipios_entidades.push(v);
        });

    function seleccionar_entidades() {

        $.ajax({
            data: {'id_municipio': municipio.val()},
            url: '/peticion_ajax/filtrar_entidades_interruptos_modificar/',
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