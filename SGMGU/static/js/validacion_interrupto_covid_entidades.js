/**
 * Created by Daniel.
 */

$(document).on('ready', function () {

    var organismo = $('#id_organismo'),
        entidad = $('#id_entidad');

    function seleccionar_entidades() {

        $.ajax({
            data: {'id_organismo': organismo.val()},
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

    $('#id_municipio').prop('disabled', true);

    if (organismo.val() !== ''){
        entidad.prop('disabled', false);
        seleccionar_entidades();
    } else{
        entidad.prop('disabled', true);
    }

    organismo.on('change', function(){
        if($(this).val() === ''){
            entidad.prop('disabled', true);
        }else{
            entidad.prop('disabled', false);
            seleccionar_entidades();
        }
    });
});