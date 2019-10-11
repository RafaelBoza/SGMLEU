/**
 * Created by Daniel.
 */

$(document).on('ready', function () {

    var organismo = $('#id_organismo'),
        municipio_entidad = $('#id_municipio_entidad'),
        entidad = $('#id_entidad'),
        municipios_entidades = [];
        municipio_entidad.find('option').each(function (k, v) {
            municipios_entidades.push(v);
        });

    function seleccionar_entidades(id_organismo) {

        if(municipio_entidad.val() === ''){
            $.ajax({
                data: {'id_organismo': id_organismo},
                url: '/peticion_ajax/',
                type: 'get',
                success: function(entidades){
                    var html = '';
                    html +=  '<option value="">-------</option>';
                    for(var i =0; i < entidades.length; i++){
                        html +=  '<option value=' + entidades[i].codigo_ent + '>' + entidades[i].e_nombre + '</option>';
                      }
                    entidad.html(html);
                }
            })
        }else {
           var codigo;

            for (var i = 0; i < municipios_entidades.length; i++) {
                if (municipios_entidades[i].dataset.id_mun === municipio_entidad.val()) {
                    codigo = municipios_entidades[i].dataset.codigo_mes;
                }
            }
            $.ajax({
                data: {'id_organismo': id_organismo, 'id_municipio_entidad': codigo},
                url: '/peticion_ajax/',
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
    }

    if(organismo.val() !== ''){

        var id_organismo = organismo.val();

        seleccionar_entidades(id_organismo);

    }

    organismo.on('change', function(){
        if($(this).val() === ''){
            entidad.prop('disabled', true);
            entidad.prop('required', false);
            municipio_entidad.prop('disabled', true);
            municipio_entidad.prop('required', false);
        }else{
            entidad.prop('disabled', false);
            entidad.prop('required', true);
            municipio_entidad.prop('disabled', false);

            var id_organismo = $(this).val();
            seleccionar_entidades(id_organismo);
        }
    });

    municipio_entidad.on('change', function(){

        var id_organismo = organismo.val();

        seleccionar_entidades(id_organismo);

    });

});