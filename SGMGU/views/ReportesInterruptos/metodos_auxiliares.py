from SGMGU.models import Organismo


def registrado_mes_actual(value, mes):
    if value.fecha_registro.month == mes:
        return True
    else:
        return False


def obtener_oaces():
    organismos = Organismo.objects.filter(activo=True)
    organismos_sin_osdes = []

    for organismo in organismos:

        id_organismo = organismo.id
        id_penultimo_digito = int(str(id_organismo)[3])
        id_ultimo_digito = int(str(id_organismo)[4])

        if id_penultimo_digito == 0 and id_ultimo_digito == 0:
            organismos_sin_osdes.append(organismo)

    return organismos_sin_osdes
    # devuelve un []


def es_oace(organismo):

    id_organismo = organismo.id
    id_penultimo_digito = int(str(id_organismo)[3])
    id_ultimo_digito = int(str(id_organismo)[4])

    if id_penultimo_digito == 0 and id_ultimo_digito == 0:
        return True
    else:
        return False


def obtener_osdes():
    oaces = obtener_oaces()
    return Organismo.objects.exclude(id__in=[oace.id for oace in oaces]).filter(activo=True)
    # devuelve un query


def obtener_osdes_de_un_oace(organismo):
    osdes = obtener_osdes()
    osdes_del_organismo = []
    for osde in osdes:
        if osde.hijode_id == organismo.id:
            osdes_del_organismo.append(osde)

    return osdes_del_organismo
    # devuelve un []


def total_interruptos(interrupto):

    return (  # hasta 30 dias
        interrupto.hastatreintadias_reubicadostemporal_misma_entidad +
        interrupto.hastatreintadias_reubicadostemporal_mismo_organismo +
        interrupto.hastatreintadias_reubicadostemporal_otro_organismo +
        interrupto.hastatreintadias_cobrandogarantiasalarial +
        interrupto.hastatreintadias_singarantiasalarial +
        interrupto.hastatreintadias_baja +
        interrupto.hastatreintadias_propuestoadisponibles +
        # entre 30 y 60 dias
        interrupto.entretreintaysesentadias_reubicadostemporal_misma_entidad +
        interrupto.entretreintaysesentadias_reubicadostemporal_mismo_organismo +
        interrupto.entretreintaysesentadias_reubicadostemporal_otro_organismo +
        interrupto.entretreintaysesentadias_cobrandogarantiasalarial +
        interrupto.entretreintaysesentadias_singarantiasalarial +
        interrupto.entretreintaysesentadias_baja +
        interrupto.entretreintaysesentadias_propuestoadisponibles +
        # mas de 60 dias y un anno
        interrupto.masdesesentayunanno_reubicadostemporal_misma_entidad +
        interrupto.masdesesentayunanno_reubicadostemporal_mismo_organismo +
        interrupto.masdesesentayunanno_reubicadostemporal_otro_organismo +
        interrupto.masdesesentayunanno_cobrandogarantiasalarial +
        interrupto.masdesesentayunanno_singarantiasalarial +
        interrupto.masdesesentayunanno_baja +
        interrupto.masdesesentayunanno_propuestoadisponibles +
        # mas de 1 anno
        interrupto.masdeunanno_reubicadostemporal_misma_entidad +
        interrupto.masdeunanno_reubicadostemporal_mismo_organismo +
        interrupto.masdeunanno_reubicadostemporal_otro_organismo +
        interrupto.masdeunanno_cobrandogarantiasalarial +
        interrupto.masdeunanno_singarantiasalarial +
        interrupto.masdeunanno_baja +
        interrupto.masdeunanno_propuestoadisponibles)


def totales_por_organismo(interruptos):

    t = 0
    t_femeninos = 0
    t_jovenes = 0
    t_hasta_treinta_dias = 0
    t_mas_treinta_menos_sesenta_dias = 0
    t_mas_sesenta_dias_menos_un_anno = 0
    t_mas_un_anno = 0
    t_reubicados_temporal_misma_entidad = 0
    t_reubicados_temporal_mismo_organismo = 0
    t_reubicados_temporal_otro_organismo = 0
    t_cobrando_garantia_salarial = 0
    t_sin_garantia_salarial = 0
    t_baja = 0
    t_propuesto_disponible = 0

    for interrupto in interruptos:
        t += total_interruptos(interrupto)

        t_femeninos += (interrupto.f_hastatreintadias_reubicadostemporal +
                        interrupto.f_hastatreintadias_cobrandogarantiasalarial +
                        interrupto.f_hastatreintadias_singarantiasalarial +
                        interrupto.f_hastatreintadias_baja +
                        interrupto.f_hastatreintadias_propuestoadisponibles +
                        interrupto.f_entretreintaysesentadias_reubicadostemporal +
                        interrupto.f_entretreintaysesentadias_cobrandogarantiasalarial +
                        interrupto.f_entretreintaysesentadias_singarantiasalarial +
                        interrupto.f_entretreintaysesentadias_baja +
                        interrupto.f_entretreintaysesentadias_propuestoadisponibles +
                        interrupto.f_masdesesentayunanno_reubicadostemporal +
                        interrupto.f_masdesesentayunanno_cobrandogarantiasalarial +
                        interrupto.f_masdesesentayunanno_singarantiasalarial +
                        interrupto.f_masdesesentayunanno_baja +
                        interrupto.f_masdesesentayunanno_propuestoadisponibles +
                        interrupto.f_masdeunanno_reubicadostemporal +
                        interrupto.f_masdeunanno_cobrandogarantiasalarial +
                        interrupto.f_masdeunanno_singarantiasalarial +
                        interrupto.f_masdeunanno_baja +
                        interrupto.f_masdeunanno_propuestoadisponibles)

        t_jovenes += (interrupto.jovenes_hastatreintadias_reubicadostemporal +
                      interrupto.jovenes_hastatreintadias_cobrandogarantiasalarial +
                      interrupto.jovenes_hastatreintadias_singarantiasalarial +
                      interrupto.jovenes_hastatreintadias_baja +
                      interrupto.jovenes_hastatreintadias_propuestoadisponibles +
                      interrupto.jovenes_entretreintaysesentadias_reubicadostemporal +
                      interrupto.jovenes_entretreintaysesentadias_cobrandogarantiasalarial +
                      interrupto.jovenes_entretreintaysesentadias_singarantiasalarial +
                      interrupto.jovenes_entretreintaysesentadias_baja +
                      interrupto.jovenes_entretreintaysesentadias_propuestoadisponibles +
                      interrupto.jovenes_masdesesentayunanno_reubicadostemporal +
                      interrupto.jovenes_masdesesentayunanno_cobrandogarantiasalarial +
                      interrupto.jovenes_masdesesentayunanno_singarantiasalarial +
                      interrupto.jovenes_masdesesentayunanno_baja +
                      interrupto.jovenes_masdesesentayunanno_propuestoadisponibles +
                      interrupto.jovenes_masdeunanno_reubicadostemporal +
                      interrupto.jovenes_masdeunanno_cobrandogarantiasalarial +
                      interrupto.jovenes_masdeunanno_singarantiasalarial +
                      interrupto.jovenes_masdeunanno_baja +
                      interrupto.jovenes_masdeunanno_propuestoadisponibles)

        t_hasta_treinta_dias += (interrupto.hastatreintadias_reubicadostemporal_misma_entidad +
                                 interrupto.hastatreintadias_reubicadostemporal_mismo_organismo +
                                 interrupto.hastatreintadias_reubicadostemporal_otro_organismo +
                                 interrupto.hastatreintadias_cobrandogarantiasalarial +
                                 interrupto.hastatreintadias_singarantiasalarial +
                                 interrupto.hastatreintadias_baja +
                                 interrupto.hastatreintadias_propuestoadisponibles)

        t_mas_treinta_menos_sesenta_dias += (interrupto.entretreintaysesentadias_reubicadostemporal_misma_entidad +
                                             interrupto.entretreintaysesentadias_reubicadostemporal_mismo_organismo +
                                             interrupto.entretreintaysesentadias_reubicadostemporal_otro_organismo +
                                             interrupto.entretreintaysesentadias_cobrandogarantiasalarial +
                                             interrupto.entretreintaysesentadias_singarantiasalarial +
                                             interrupto.entretreintaysesentadias_baja +
                                             interrupto.entretreintaysesentadias_propuestoadisponibles)

        t_mas_sesenta_dias_menos_un_anno += (interrupto.masdesesentayunanno_reubicadostemporal_misma_entidad +
                                             interrupto.masdesesentayunanno_reubicadostemporal_mismo_organismo +
                                             interrupto.masdesesentayunanno_reubicadostemporal_otro_organismo +
                                             interrupto.masdesesentayunanno_cobrandogarantiasalarial +
                                             interrupto.masdesesentayunanno_singarantiasalarial +
                                             interrupto.masdesesentayunanno_baja +
                                             interrupto.masdesesentayunanno_propuestoadisponibles)

        t_mas_un_anno += (interrupto.masdeunanno_reubicadostemporal_misma_entidad +
                          interrupto.masdeunanno_reubicadostemporal_mismo_organismo +
                          interrupto.masdeunanno_reubicadostemporal_otro_organismo +
                          interrupto.masdeunanno_cobrandogarantiasalarial +
                          interrupto.masdeunanno_singarantiasalarial +
                          interrupto.masdeunanno_baja +
                          interrupto.masdeunanno_propuestoadisponibles)

        t_reubicados_temporal_misma_entidad += (interrupto.hastatreintadias_reubicadostemporal_misma_entidad +
                                                interrupto.entretreintaysesentadias_reubicadostemporal_misma_entidad +
                                                interrupto.masdesesentayunanno_reubicadostemporal_misma_entidad +
                                                interrupto.masdeunanno_reubicadostemporal_misma_entidad)

        t_reubicados_temporal_mismo_organismo += (interrupto.hastatreintadias_reubicadostemporal_mismo_organismo +
                                                  interrupto.entretreintaysesentadias_reubicadostemporal_mismo_organismo +
                                                  interrupto.masdesesentayunanno_reubicadostemporal_mismo_organismo +
                                                  interrupto.masdeunanno_reubicadostemporal_mismo_organismo)

        t_reubicados_temporal_otro_organismo += (interrupto.hastatreintadias_reubicadostemporal_otro_organismo +
                                                 interrupto.entretreintaysesentadias_reubicadostemporal_otro_organismo +
                                                 interrupto.masdesesentayunanno_reubicadostemporal_otro_organismo +
                                                 interrupto.masdeunanno_reubicadostemporal_otro_organismo)

        t_cobrando_garantia_salarial += (interrupto.hastatreintadias_cobrandogarantiasalarial +
                                         interrupto.entretreintaysesentadias_cobrandogarantiasalarial +
                                         interrupto.masdesesentayunanno_cobrandogarantiasalarial +
                                         interrupto.masdeunanno_cobrandogarantiasalarial)

        t_sin_garantia_salarial += (interrupto.hastatreintadias_singarantiasalarial +
                                    interrupto.entretreintaysesentadias_singarantiasalarial +
                                    interrupto.masdesesentayunanno_singarantiasalarial +
                                    interrupto.masdeunanno_singarantiasalarial)

        t_baja += (interrupto.hastatreintadias_baja +
                   interrupto.entretreintaysesentadias_baja +
                   interrupto.masdesesentayunanno_baja +
                   interrupto.masdeunanno_baja)

        t_propuesto_disponible += (interrupto.hastatreintadias_propuestoadisponibles +
                                   interrupto.entretreintaysesentadias_propuestoadisponibles +
                                   interrupto.masdesesentayunanno_propuestoadisponibles +
                                   interrupto.masdeunanno_propuestoadisponibles)

    totales = {
        't': t,
        't_femeninos': t_femeninos,
        't_jovenes': t_jovenes,
        't_hasta_treinta_dias': t_hasta_treinta_dias,
        't_mas_treinta_menos_sesenta_dias': t_mas_treinta_menos_sesenta_dias,
        't_mas_sesenta_dias_menos_un_anno': t_mas_sesenta_dias_menos_un_anno,
        't_mas_un_anno': t_mas_un_anno,
        't_reubicados_temporal_misma_entidad': t_reubicados_temporal_misma_entidad,
        't_reubicados_temporal_mismo_organismo': t_reubicados_temporal_mismo_organismo,
        't_reubicados_temporal_otro_organismo': t_reubicados_temporal_otro_organismo,
        't_cobrando_garantia_salarial': t_cobrando_garantia_salarial,
        't_sin_garantia_salarial': t_sin_garantia_salarial,
        't_baja': t_baja,
        't_propuesto_disponible': t_propuesto_disponible,
    }

    return totales


def total_interruptos_por_entidad(interrupto):
    suma = (interrupto.hastatreintadias_reubicadostemporal_misma_entidad +
            interrupto.hastatreintadias_reubicadostemporal_mismo_organismo +
            interrupto.hastatreintadias_reubicadostemporal_otro_organismo +
            interrupto.hastatreintadias_cobrandogarantiasalarial +
            interrupto.hastatreintadias_singarantiasalarial +
            interrupto.hastatreintadias_baja +
            interrupto.hastatreintadias_propuestoadisponibles +
            interrupto.entretreintaysesentadias_reubicadostemporal_misma_entidad +
            interrupto.entretreintaysesentadias_reubicadostemporal_mismo_organismo +
            interrupto.entretreintaysesentadias_reubicadostemporal_otro_organismo +
            interrupto.entretreintaysesentadias_cobrandogarantiasalarial +
            interrupto.entretreintaysesentadias_singarantiasalarial +
            interrupto.entretreintaysesentadias_baja +
            interrupto.entretreintaysesentadias_propuestoadisponibles +
            interrupto.masdesesentayunanno_reubicadostemporal_misma_entidad +
            interrupto.masdesesentayunanno_reubicadostemporal_mismo_organismo +
            interrupto.masdesesentayunanno_reubicadostemporal_otro_organismo +
            interrupto.masdesesentayunanno_cobrandogarantiasalarial +
            interrupto.masdesesentayunanno_singarantiasalarial +
            interrupto.masdesesentayunanno_baja +
            interrupto.masdesesentayunanno_propuestoadisponibles +
            interrupto.masdeunanno_reubicadostemporal_misma_entidad +
            interrupto.masdeunanno_reubicadostemporal_mismo_organismo +
            interrupto.masdeunanno_reubicadostemporal_otro_organismo +
            interrupto.masdeunanno_cobrandogarantiasalarial +
            interrupto.masdeunanno_singarantiasalarial +
            interrupto.masdeunanno_baja +
            interrupto.masdeunanno_propuestoadisponibles)

    return suma


def total_femeninos_interruptos_por_entidad(interrupto):
    suma = (interrupto.f_hastatreintadias_reubicadostemporal +
            interrupto.f_hastatreintadias_cobrandogarantiasalarial +
            interrupto.f_hastatreintadias_singarantiasalarial +
            interrupto.f_hastatreintadias_baja +
            interrupto.f_hastatreintadias_propuestoadisponibles +
            interrupto.f_entretreintaysesentadias_reubicadostemporal +
            interrupto.f_entretreintaysesentadias_cobrandogarantiasalarial +
            interrupto.f_entretreintaysesentadias_singarantiasalarial +
            interrupto.f_entretreintaysesentadias_baja +
            interrupto.f_entretreintaysesentadias_propuestoadisponibles +
            interrupto.f_masdesesentayunanno_reubicadostemporal +
            interrupto.f_masdesesentayunanno_cobrandogarantiasalarial +
            interrupto.f_masdesesentayunanno_singarantiasalarial +
            interrupto.f_masdesesentayunanno_baja +
            interrupto.f_masdesesentayunanno_propuestoadisponibles +
            interrupto.f_masdeunanno_reubicadostemporal +
            interrupto.f_masdeunanno_cobrandogarantiasalarial +
            interrupto.f_masdeunanno_singarantiasalarial +
            interrupto.f_masdeunanno_baja +
            interrupto.f_masdeunanno_propuestoadisponibles)

    return suma


def total_jovenes_interruptos_por_entidad(interrupto):
    suma = (interrupto.jovenes_hastatreintadias_reubicadostemporal +
            interrupto.jovenes_hastatreintadias_cobrandogarantiasalarial +
            interrupto.jovenes_hastatreintadias_singarantiasalarial +
            interrupto.jovenes_hastatreintadias_baja +
            interrupto.jovenes_hastatreintadias_propuestoadisponibles +
            interrupto.jovenes_entretreintaysesentadias_reubicadostemporal +
            interrupto.jovenes_entretreintaysesentadias_cobrandogarantiasalarial +
            interrupto.jovenes_entretreintaysesentadias_singarantiasalarial +
            interrupto.jovenes_entretreintaysesentadias_baja +
            interrupto.jovenes_entretreintaysesentadias_propuestoadisponibles +
            interrupto.jovenes_masdesesentayunanno_reubicadostemporal +
            interrupto.jovenes_masdesesentayunanno_cobrandogarantiasalarial +
            interrupto.jovenes_masdesesentayunanno_singarantiasalarial +
            interrupto.jovenes_masdesesentayunanno_baja +
            interrupto.jovenes_masdesesentayunanno_propuestoadisponibles +
            interrupto.jovenes_masdeunanno_reubicadostemporal +
            interrupto.jovenes_masdeunanno_cobrandogarantiasalarial +
            interrupto.jovenes_masdeunanno_singarantiasalarial +
            interrupto.jovenes_masdeunanno_baja +
            interrupto.jovenes_masdeunanno_propuestoadisponibles)

    return suma


def interruptos_hasta_treinta_dias_por_entidad(interrupto):
    suma = (interrupto.hastatreintadias_reubicadostemporal_misma_entidad +
            interrupto.hastatreintadias_reubicadostemporal_mismo_organismo +
            interrupto.hastatreintadias_reubicadostemporal_otro_organismo +
            interrupto.hastatreintadias_cobrandogarantiasalarial +
            interrupto.hastatreintadias_singarantiasalarial +
            interrupto.hastatreintadias_baja +
            interrupto.hastatreintadias_propuestoadisponibles)

    return suma


def interruptos_mas_treinta_hasta_sesenta_por_entidad(interrupto):
    suma = (interrupto.entretreintaysesentadias_reubicadostemporal_misma_entidad +
            interrupto.entretreintaysesentadias_reubicadostemporal_mismo_organismo +
            interrupto.entretreintaysesentadias_reubicadostemporal_otro_organismo +
            interrupto.entretreintaysesentadias_cobrandogarantiasalarial +
            interrupto.entretreintaysesentadias_singarantiasalarial +
            interrupto.entretreintaysesentadias_baja +
            interrupto.entretreintaysesentadias_propuestoadisponibles)

    return suma


def interruptos_mas_sesenta_menos_un_anno_por_entidad(interrupto):
    suma = (interrupto.masdesesentayunanno_reubicadostemporal_misma_entidad +
            interrupto.masdesesentayunanno_reubicadostemporal_mismo_organismo +
            interrupto.masdesesentayunanno_reubicadostemporal_otro_organismo +
            interrupto.masdesesentayunanno_cobrandogarantiasalarial +
            interrupto.masdesesentayunanno_singarantiasalarial +
            interrupto.masdesesentayunanno_baja +
            interrupto.masdesesentayunanno_propuestoadisponibles)

    return suma


def interruptos_mas_un_anno_por_entidad(interrupto):
    suma = (interrupto.masdeunanno_reubicadostemporal_misma_entidad +
            interrupto.masdeunanno_reubicadostemporal_mismo_organismo +
            interrupto.masdeunanno_reubicadostemporal_otro_organismo +
            interrupto.masdeunanno_cobrandogarantiasalarial +
            interrupto.masdeunanno_singarantiasalarial +
            interrupto.masdeunanno_baja +
            interrupto.masdeunanno_propuestoadisponibles)

    return suma


def interruptos_reubicado_misma_entidad_por_entidad(interrupto):
    suma = (interrupto.hastatreintadias_reubicadostemporal_misma_entidad +
            interrupto.entretreintaysesentadias_reubicadostemporal_misma_entidad +
            interrupto.masdesesentayunanno_reubicadostemporal_misma_entidad +
            interrupto.masdeunanno_reubicadostemporal_misma_entidad)

    return suma


def interruptos_reubicado_mismo_organismo_por_entidad(interrupto):
    suma = (interrupto.hastatreintadias_reubicadostemporal_mismo_organismo +
            interrupto.entretreintaysesentadias_reubicadostemporal_mismo_organismo +
            interrupto.masdesesentayunanno_reubicadostemporal_mismo_organismo +
            interrupto.masdeunanno_reubicadostemporal_mismo_organismo)

    return suma


def interruptos_reubicado_otro_organismo_por_entidad(interrupto):
    suma = (interrupto.hastatreintadias_reubicadostemporal_otro_organismo +
            interrupto.entretreintaysesentadias_reubicadostemporal_otro_organismo +
            interrupto.masdesesentayunanno_reubicadostemporal_otro_organismo +
            interrupto.masdeunanno_reubicadostemporal_otro_organismo)

    return suma


def interruptos_cobrando_garantia_salarial_por_entidad(interrupto):
    suma = (interrupto.hastatreintadias_cobrandogarantiasalarial +
            interrupto.entretreintaysesentadias_cobrandogarantiasalarial +
            interrupto.masdesesentayunanno_cobrandogarantiasalarial +
            interrupto.masdeunanno_cobrandogarantiasalarial)

    return suma


def interruptos_sin_garantia_salarial_por_entidad(interrupto):
    suma = (interrupto.hastatreintadias_singarantiasalarial +
            interrupto.entretreintaysesentadias_singarantiasalarial +
            interrupto.masdesesentayunanno_singarantiasalarial +
            interrupto.masdeunanno_singarantiasalarial)

    return suma


def interruptos_baja_por_entidad(interrupto):
    suma = (interrupto.hastatreintadias_baja +
            interrupto.entretreintaysesentadias_baja +
            interrupto.masdesesentayunanno_baja +
            interrupto.masdeunanno_baja)

    return suma


def interruptos_propuesto_disponible_por_entidad(interrupto):
    suma = (interrupto.hastatreintadias_propuestoadisponibles +
            interrupto.entretreintaysesentadias_propuestoadisponibles +
            interrupto.masdesesentayunanno_propuestoadisponibles +
            interrupto.masdeunanno_propuestoadisponibles)

    return suma


def totales_interruptos_organismo_provincia(interruptos, organismo, provincia):

    cantidad = 0

    for interrupto in interruptos:
        if interrupto.organismo == organismo and interrupto.municipio.provincia == provincia:
            cantidad += total_interruptos(interrupto)

    return cantidad


# def totales_interruptos_organismo_actividades(interruptos, organismo, actividad):
#
#     cantidad = 0
#     interruptos = interruptos.filter(organismo=organismo, actividad=actividad)
#
#     for interrupto in interruptos:
#         cantidad += total_interruptos(interrupto)
#
#     return cantidad


def totales_interruptos_organismo_actividades(interruptos, organismo, actividad):

    cantidad = 0
    interruptos = interruptos.filter(organismo=organismo)

    if actividad.id == 2:
        for interrupto in interruptos:
            cantidad += interrupto.actividad_directos
    # if actividad.id == 3:
    #     for interrupto in interruptos:
    #         cantidad += interrupto.actividad_todos
    if actividad.id == 4:
        for interrupto in interruptos:
            cantidad += interrupto.actividad_indirectos

    return cantidad


def totales_interruptos_actividades(interrupto, actividad):


    if actividad.id == 2:
        return interrupto.actividad_directos
    # if actividad.id == 3:
    #     return interrupto.actividad_todos
    if actividad.id == 4:
        return interrupto.actividad_indirectos


def totales_interruptos_organismo_causas_interrupcion(interruptos, organismo, id_causa_interrupcion):

    cantidad = 0
    interruptos = interruptos.filter(organismo=organismo)

    if id_causa_interrupcion == 1:
        for interrupto in interruptos:
            cantidad += interrupto.causa_interrupcion_rotura

    if id_causa_interrupcion == 2:
        for interrupto in interruptos:
            cantidad += interrupto.causa_interrupcion_falta_piezas

    if id_causa_interrupcion == 3:
        for interrupto in interruptos:
            cantidad += interrupto.causa_interrupcion_accion_lluvia

    if id_causa_interrupcion == 4:
        for interrupto in interruptos:
            cantidad += interrupto.causa_interrupcion_falta_energia

    if id_causa_interrupcion == 5:
        for interrupto in interruptos:
            cantidad += interrupto.causa_interrupcion_orden_paralizacion_temporal

    if id_causa_interrupcion == 6:
        for interrupto in interruptos:
            cantidad += interrupto.causa_interrupcion_paralizacion_reparacion

    if id_causa_interrupcion == 7:
        for interrupto in interruptos:
            cantidad += interrupto.causa_interrupcion_otras_causas

    return cantidad


def totales_interruptos_causas_interrupcion(interrupto, id_causa_interrupcion):

    if id_causa_interrupcion == 1:
        return interrupto.causa_interrupcion_rotura

    if id_causa_interrupcion == 2:
        return interrupto.causa_interrupcion_falta_piezas

    if id_causa_interrupcion == 3:
        return interrupto.causa_interrupcion_accion_lluvia

    if id_causa_interrupcion == 4:
        return interrupto.causa_interrupcion_falta_energia

    if id_causa_interrupcion == 5:
        return interrupto.causa_interrupcion_orden_paralizacion_temporal

    if id_causa_interrupcion == 6:
        return interrupto.causa_interrupcion_paralizacion_reparacion

    if id_causa_interrupcion == 7:
        return interrupto.causa_interrupcion_otras_causas


def totales_situacion_tiempo(listado_interruptos):

    total = 0
    hasta_treinta_dias_misma_entidad = 0
    hasta_treinta_dias_mismo_organismo = 0
    hasta_treinta_dias_otro_organismo = 0
    mas_treinta_misma_entidad = 0
    mas_treinta_mismo_organismo = 0
    mas_treinta_otro_organismo = 0
    mas_sesenta_misma_entidad = 0
    mas_sesenta_mismo_organismo = 0
    mas_sesenta_otro_organismo = 0
    mas_un_anno_misma_entidad = 0
    mas_un_anno_mismo_organismo = 0
    mas_un_anno_otro_organismo = 0

    for interrupto in listado_interruptos:

        total += interrupto['total_interruptos_entidad']
        hasta_treinta_dias_misma_entidad += interrupto['hastatreintadias_reubicadostemporal_misma_entidad']
        hasta_treinta_dias_mismo_organismo += interrupto['hastatreintadias_reubicadostemporal_mismo_organismo']
        hasta_treinta_dias_otro_organismo += interrupto['hastatreintadias_reubicadostemporal_otro_organismo']
        mas_treinta_misma_entidad += interrupto['entretreintaysesentadias_reubicadostemporal_misma_entidad']
        mas_treinta_mismo_organismo += interrupto['entretreintaysesentadias_reubicadostemporal_mismo_organismo']
        mas_treinta_otro_organismo += interrupto['entretreintaysesentadias_reubicadostemporal_otro_organismo']
        mas_sesenta_misma_entidad += interrupto['masdesesentayunanno_reubicadostemporal_misma_entidad']
        mas_sesenta_mismo_organismo += interrupto['masdesesentayunanno_reubicadostemporal_mismo_organismo']
        mas_sesenta_otro_organismo += interrupto['masdesesentayunanno_reubicadostemporal_otro_organismo']
        mas_un_anno_misma_entidad += interrupto['masdeunanno_reubicadostemporal_misma_entidad']
        mas_un_anno_mismo_organismo += interrupto['masdeunanno_reubicadostemporal_mismo_organismo']
        mas_un_anno_otro_organismo += interrupto['masdeunanno_reubicadostemporal_otro_organismo']

    totales = {
        'total': total,
        'hasta_treinta_dias_misma_entidad': hasta_treinta_dias_misma_entidad,
        'hasta_treinta_dias_mismo_organismo': hasta_treinta_dias_mismo_organismo,
        'hasta_treinta_dias_otro_organismo': hasta_treinta_dias_otro_organismo,
        'mas_treinta_misma_entidad': mas_treinta_misma_entidad,
        'mas_treinta_mismo_organismo': mas_treinta_mismo_organismo,
        'mas_treinta_otro_organismo': mas_treinta_otro_organismo,
        'mas_sesenta_misma_entidad': mas_sesenta_misma_entidad,
        'mas_sesenta_mismo_organismo': mas_sesenta_mismo_organismo,
        'mas_sesenta_otro_organismo': mas_sesenta_otro_organismo,
        'mas_un_anno_misma_entidad': mas_un_anno_misma_entidad,
        'mas_un_anno_mismo_organismo': mas_un_anno_mismo_organismo,
        'mas_un_anno_otro_organismo': mas_un_anno_otro_organismo
    }

    return totales
