from SGMGU.models import Ubicacion, CausalNoUbicado


def diccionario_totales(listado, mes, anno):

    controlados = 0
    ubicados = 0
    l_ubicaciones = Ubicacion.objects.filter(activo=True)
    ubicaciones = {}
    for ubicacion in l_ubicaciones:
        ubicaciones[str(ubicacion.id)] = 0
    no_ubicados = 0
    l_causas_no_ubicado = CausalNoUbicado.objects.filter(activo=True)
    causas_no_ubicado = {}
    for causa in l_causas_no_ubicado:
        causas_no_ubicado[str(causa.id)] = 0

    for persona in listado:
        if persona.fecha_registro.month < mes and persona.fecha_registro.year == anno:
            controlados += 1

            try:
                if persona.ubicado:
                    ubicados += 1
                elif not persona.ubicado:
                    no_ubicados += 1
            except: pass

            if persona.ubicacion:
                ubicaciones[str(persona.ubicacion.id)] += 1

            if persona.causa_no_ubicado:
                causas_no_ubicado[str(persona.causa_no_ubicado.id)] += 1

        elif persona.fecha_registro.year != anno:
            controlados += 1

            try:
                if persona.ubicado:
                    ubicados += 1
                elif not persona.ubicado:
                    no_ubicados += 1
            except: pass

            if persona.ubicacion:
                ubicaciones[str(persona.ubicacion.id)] += 1

            if persona.causa_no_ubicado:
                causas_no_ubicado[str(persona.causa_no_ubicado.id)] += 1

    return {
        'controlados': controlados,
        'ubicados': ubicados,
        'ubicaciones': ubicaciones,
        'no_ubicados': no_ubicados,
        'causas_no_ubicado': causas_no_ubicado,
    }
