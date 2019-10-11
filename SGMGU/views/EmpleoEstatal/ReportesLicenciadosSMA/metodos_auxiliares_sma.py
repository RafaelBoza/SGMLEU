def controlados_provincia(licenciados):

    controlados = 0
    controlados_femeninos = 0
    incorporados = 0
    incorporados_femeninos = 0
    empleo_estatal = 0
    tpcp = 0
    dl_358 = 0
    otra_no_estatal = 0
    no_incorporados = 0
    no_incorporados_femeninos = 0

    for l in licenciados:
        if l['incorporado']:
            controlados += 1

            if l['incorporado'] == 1:
                incorporados += 1

                if l['sexo'] == 'F':
                    controlados_femeninos += 1
                    incorporados_femeninos += 1

                if l['ubicacion'] == 1:
                    empleo_estatal += 1

                if l['ubicacion'] == 2:
                    tpcp += 1

                if l['ubicacion'] == 3:
                    dl_358 += 1

                if l['ubicacion'] == 4:
                    otra_no_estatal += 1

            elif l['incorporado'] == 2:
                no_incorporados += 1

                if l['sexo'] == 'F':
                    controlados_femeninos += 1
                    no_incorporados_femeninos += 1

    totales = {
        'controlados': controlados,
        'controlados_femeninos': controlados_femeninos,
        'incorporados': incorporados,
        'incorporados_femeninos': incorporados_femeninos,
        'empleo_estatal': empleo_estatal,
        'tpcp': tpcp,
        'dl_358': dl_358,
        'otra_no_estatal': otra_no_estatal,
        'no_incorporados': no_incorporados,
        'no_incorporados_femeninos': no_incorporados_femeninos,
    }

    return totales


def resultados_entrevistas_provincia(lista_licenciados_sma):

    controlados = lista_licenciados_sma.count()
    recibio_oferta = 0
    acepto_oferta = 0
    empleo_estatal = 0
    tpcp = 0
    dl_358 = 0
    otra_no_estatal = 0
    no_acepto_oferta = 0
    no_le_gustan_las_ofertas = 0
    no_desea_trabajar = 0

    for licenciado in lista_licenciados_sma:

        if licenciado['recibio_oferta']:
            recibio_oferta += 1

            if licenciado['acepto_oferta'] == 'S':
                acepto_oferta += 1

                if licenciado['ubicacion'] == 1:
                    empleo_estatal += 1

                if licenciado['ubicacion'] == 2:
                    tpcp += 1

                if licenciado['ubicacion'] == 3:
                    dl_358 += 1

                if licenciado['ubicacion'] == 4:
                    otra_no_estatal += 1

            if licenciado['acepto_oferta'] == 'N':
                no_acepto_oferta += 1

                if licenciado['causa_no_aceptacion'] == 1:
                    no_le_gustan_las_ofertas += 1

                if licenciado['causa_no_aceptacion'] == 2:
                    no_desea_trabajar += 1

    totales = {
        'controlados': controlados,
        'recibio_oferta': recibio_oferta,
        'acepto_oferta': acepto_oferta,
        'empleo_estatal': empleo_estatal,
        'tpcp': tpcp,
        'dl_358': dl_358,
        'otra_no_estatal': otra_no_estatal,
        'no_acepto_oferta': no_acepto_oferta,
        'no_le_gustan_las_ofertas': no_le_gustan_las_ofertas,
        'no_desea_trabajar': no_desea_trabajar,
    }

    return totales
