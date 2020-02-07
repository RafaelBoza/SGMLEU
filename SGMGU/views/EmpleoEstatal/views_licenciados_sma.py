# -*- coding: utf-8 -*-
import threading

from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required()
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def listado_licenciados_sma(request, errors=None):
    fecha_actual = datetime.datetime.today()
    anno_actual = fecha_actual.year
    mes_actual = fecha_actual.month
    dia_actual = fecha_actual.day

    # lic = LicenciadosSMA.objects.filter(municipio_residencia__nombre='Cotorro', activo=False).first()
    # print("CI: ", lic.ci)

    # cantidad = 0
    # controlados_incorporados = 0
    # lic = LicenciadosSMA.objects.filter(mes_entrevista='Junio', anno_entrevista=2018, activo=True)
    # print lic.count()
    # controlado = ''
    # l_incorporado = ''
    # for indice, l in enumerate(lic):
    #     c = ControlLicenciadosSMA.objects.filter(licenciado_sma_id=l.id)
    #     if c.count() > 0:
    #         cantidad += 1
    #         controlado = 'Si controlado'
    #         if c.last().incorporado == 'S':
    #             controlados_incorporados += 1
    #             l_incorporado = 'Si incorporado'
    #         else:
    #             l_incorporado = 'No incorporado'
    #     else:
    #         controlado = 'No controlado'
    #         l_incorporado = 'No incorporado'
    #     print "{} | {} | {} | {} | {} | {} | {}".format(str(indice + 1), l.ci, l.nombre_apellidos.encode('utf-8').strip(), l.municipio_residencia.provincia.nombre.encode('utf-8').strip(), l.municipio_residencia.nombre.encode('utf-8').strip(), controlado, l_incorporado)

        # if li.incorporado == 'S':
        #     cantidad += 1
            # li.activo = False
            # li.causa_baja = CausalBaja.objects.get(id=10)
            # li.fecha_baja = fecha_actual
    # print "controlados: ", cantidad
    # print "controlados incorporados: ", controlados_incorporados

    # cantidad_c = 0
    # for li in lic:
    #     controls = ControlLicenciadosSMA.objects.filter(licenciado_sma__id=li.id).order_by('id')
    #     if controls.count() > 0:
    #         ultimo_control = controls.last()
    #         if ultimo_control.incorporado == 'S':
    #             cantidad_c += 1
    #             if li.ci == '98011719022':
    #                 print "si tiene control"
    #
    # print cantidad_c

    # listado = LicenciadosSMA.objects.filter(fecha_registro__year=anno_actual) | \
    #             LicenciadosSMA.objects.filter(activo=True)
    #
    # print listado.filter(incorporado=2, municipio_residencia__id=38).count()
    #
    # for x in listado.filter(incorporado=2, causa_no_ubicado_id__in=[10], municipio_residencia__id=38):
    #     print x.ci

    # 1 caso no recibio oferta y si la acepto: 99100717229

    # 75 casos aceptaron la oferta y no tienen ubicacion:
    # ['97041017207', '96121919180', '98031721069', '97052517781', '96020318746', '97090317785', '97092216888',
    #  '98100818026', '98101416762', '97062917145', '97051521062', '96080823329', '98070805783', '98080217140',
    #  '98072316748', '98060518075', '97102616887', '97101417808', '97093017782', '98082818027', '98012318023',
    #  '98072516801', '98063016802', '98061405869', '98071805867', '98100705883', '97022205867', '97110721387',
    #  '98030721363', '98120921441', '98090821447', '98100717149', '98080317148', '98041919783', '96110506364',
    #  '98011404863', '98101704589', '98101504701', '98021404603', '98121917186', '98032417546', '99041816984',
    #  '98050817168', '98090517180', '99032816985', '97061417168', '98111617205', '99041317024', '98080217160',
    #  '97100217140', '98080217144', '97050217165', '98101216803', '97091617146', '98111505864', '99020817624',
    #  '96100319189', '95072547423', '98082512605', '98071615768', '98022516762', '99021517023', '98061217143',
    #  '96121321387', '97111304829', '99022020443', '99012304421', '98102716783', '98120118022', '98071816745',
    #  '98092105866', '98120804607', '97070812723', '98073112587', '98042421068']

    # 34 casos no aceptaron la oferta y no tienen causa de no aceptacion:
    # ['97040605463', '96112323487', '97113021086', '97110720983', '95121248166', '98101319245', '97121220904',
    #  '91083124923', '97092505288', '97042104603', '98090122749', '97092904267', '98111920022', '98100901502',
    #  '98050220028', '98072220028', '96051022360', '98070700708', '97040105641', '98032411142', '98040200901',
    #  '96070526420', '98072122042', '97022620340', '96092218784', '95102541946', '97091508662', '98112021546',
    #  '98091303625', '97083021462', '99052320903', '99020207485', '99021507549', '98101522903']

    # 2 casos en mayabeque no incorporados por: "Al cuidado de un familiar": 98091621788, 97110404642
    # 2 casos en mayabeque no incorporados por: "Lo dejo": 98041919783, 99022605722


    # lic = LicenciadosSMA.objects.all()
    # for l in lic:
    #     controles = ControlLicenciadosSMA.objects.filter(licenciado_sma__id=l.id).order_by('id')
    #     if controles.count() > 0:
    #         ultimo_control = controles.last()
    #         if ultimo_control.incorporado == 'S':
    #             l.incorporado = EstadoIncorporado.objects.get(id=1)
    #         else:
    #             l.incorporado = EstadoIncorporado.objects.get(id=2)
    #         if ultimo_control.ubicacion:
    #             l.ubicacion = ultimo_control.ubicacion
    #         l.save()

    # lic = LicenciadosSMA.objects.all()
    # for l in lic:
    #     controles = ControlLicenciadosSMA.objects.filter(licenciado_sma__id=l.id).order_by('id')
    #     if controles.count() > 0:
    #         ultimo_control = controles.last()
    #         l.organismo = ultimo_control.organismo
    #         l.entidad = ultimo_control.entidad
    #         l.municipio_entidad = ultimo_control.municipio
    #         l.save()

    # lic = LicenciadosSMA.objects.all()
    # for l in lic:
    #     controles = ControlLicenciadosSMA.objects.filter(licenciado_sma__id=l.id).order_by('id')
    #     if controles.count() > 0:
    #         ultimo_control = controles.last()
    #         l.causa_no_ubicado = ultimo_control.causa_no_ubicado
    #         l.save()

    # lic = LicenciadosSMA.objects.filter(activo=True)
    # for l in lic:
    #     controles = ControlLicenciadosSMA.objects.filter(licenciado_sma__id=l.id).order_by('id')
    #     if controles.count() > 0:
    #         ultimo_control = controles.last()
    #         if ultimo_control.incorporado == 'S' and ultimo_control.organismo is None and ultimo_control.ubicacion is not None:
    #             if ultimo_control.ubicacion.id == 1:
    #                 print l.ci

    # -------------------------------------------------------------------------------------

    # No recibieron oferta
    # lic = LicenciadosSMA.objects.filter(recibio_oferta=False, activo=True)
    # for l in lic:
    #     l.ubicacion = Ubicacion.objects.get(id=1)
    #     l.save()

    # Recibieron oferta, no la aceptaron y no tienen ubicacion
    # lic = LicenciadosSMA.objects.filter(recibio_oferta=True, acepto_oferta='N', ubicacion=None, activo=True)
    # for l in lic:
    #     l.ubicacion = Ubicacion.objects.get(id=1)
    #     l.save()

    # Recibio la oferta, acepto la oferta y no tiene ubicacion
    # lic = LicenciadosSMA.objects.filter(recibio_oferta=True, acepto_oferta='S', ubicacion=None, activo=True)
    # for l in lic:
    #     l.ubicacion = Ubicacion.objects.get(id=1)
    #     l.save()

    # Recibieron oferta y dejaron vacio el campo de aceptar la oferta
    # lic = LicenciadosSMA.objects.filter(recibio_oferta=True, acepto_oferta='', activo=True)
    # for l in lic:
    #     l.ubicacion = Ubicacion.objects.get(id=1)
    #     l.save()

    if 11 <= dia_actual <= 18 and mes_actual == 1:

        comprobado = ComprobacionAnualEmpleoEstatal.objects.filter(fuente_procedencia_id=1,
                                                                   fecha_comprobacion__year=anno_actual)

        if comprobado.count() == 0:

            licenciados = LicenciadosSMA.objects.filter(activo=True).exclude(fecha_registro__year=anno_actual)

            ids = []
            for l in licenciados:
                controles = ControlLicenciadosSMA.objects.filter(licenciado_sma=l)
                if controles.count() > 0:
                    incorporado = False
                    for c in controles:
                        if incorporado:
                            break
                        elif c.incorporado == 'S':
                            ids.append(l.id)
                            incorporado = True

            comprobar_pendientes(LicenciadosSMA.objects.filter(id__in=ids))

            ComprobacionAnualEmpleoEstatal.objects.create(fuente_procedencia_id=1, fecha_comprobacion=anno_actual)

    if request.user.perfil_usuario.categoria.nombre == 'dmt':
        licenciados_sma = LicenciadosSMA.objects.filter(municipio_residencia=request.user.perfil_usuario.municipio,
                                                        fecha_registro__year=anno_actual) | \
                          LicenciadosSMA.objects.filter(municipio_residencia=request.user.perfil_usuario.municipio,
                                                        activo=True)
    elif request.user.perfil_usuario.categoria.nombre == 'dpt_ee':
        licenciados_sma = LicenciadosSMA.objects.filter(municipio_residencia__provincia=request.user.perfil_usuario.provincia,
                                                        fecha_registro__year=anno_actual) | \
                          LicenciadosSMA.objects.filter(municipio_residencia=request.user.perfil_usuario.municipio,
                                                        activo=True)
    else:
        licenciados_sma = LicenciadosSMA.objects.all()

    licenciados_sma = paginar(request, licenciados_sma)
    paginas = crear_lista_pages(licenciados_sma)

    context = {'errors': errors, 'licenciados_sma': licenciados_sma, 'nombre_pag': "Listado: Licenciados del SMA",
               'tab': 'listar_licenciados_sma', 'paginas': paginas}
    return render(request, "EmpleoEstatal/LicenciadosSMA/listar_licenciados_sma.html", context)


@login_required
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def buscar_ci_licenciados_sma(request, ci):
    categoria_usuario = request.user.perfil_usuario.categoria.nombre
    municipio_usuario = request.user.perfil_usuario.municipio
    provincia_usuario = request.user.perfil_usuario.provincia
    anno_actual = datetime.date.today().year

    if categoria_usuario == 'dmt':
        licenciados_sma = LicenciadosSMA.objects.filter(ci__contains=ci, municipio_residencia=municipio_usuario,
                                                        fecha_registro__year=anno_actual) | \
                          LicenciadosSMA.objects.filter(ci__contains=ci, municipio_residencia=municipio_usuario,
                                                        activo=True)
    elif categoria_usuario == 'dpt_ee':
        licenciados_sma = LicenciadosSMA.objects.filter(ci__contains=ci,
                                                        municipio_residencia__provincia=provincia_usuario,
                                                        fecha_registro__year=anno_actual) | \
                          LicenciadosSMA.objects.filter(ci__contains=ci,
                                                        municipio_residencia__provincia=provincia_usuario,
                                                        activo=True)
    else:
        licenciados_sma = LicenciadosSMA.objects.filter(ci__contains=ci)

    licenciados_sma = paginar(request, licenciados_sma)
    paginas = crear_lista_pages(licenciados_sma)

    context = {'licenciados_sma': licenciados_sma, 'nombre_pag': "Listado por ci: %s" % ci,
               'busqueda': 'si', 'valor_busqueda': ci, 'paginas': paginas}
    return render(request, "EmpleoEstatal/LicenciadosSMA/listar_licenciados_sma.html", context)



@login_required
@permission_required(['administrador', 'dmt'])
def registrar_licenciado_sma(request):
    fecha_actual = datetime.datetime.now()
    carreras = Carrera.objects.filter(activo=True)
    causa_no_acep = CausalNoAceptacion.objects.filter(activo=True)
    ids_ubicaciones = [1, 2, 3, 4]
    ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
    municipio_residencia = request.user.perfil_usuario.municipio
    municipios = Municipio.objects.all()
    if request.method == 'POST':
        form = LicenciadosSMAForm(request.POST)

        recibio_oferta = ''
        acepto_oferta = ''
        ubicacion = ''

        if 'recibio_oferta' in request.POST:
            recibio_oferta = request.POST['recibio_oferta']
        if 'acepto_oferta' in request.POST:
            acepto_oferta = request.POST['acepto_oferta']
        if 'ubicacion' in request.POST:
            ubicacion = request.POST['ubicacion']

        if recibio_oferta and acepto_oferta == 'S' and ubicacion == '':
            form.add_error('ubicacion', 'Complete este campo.')

        nivel_escolar = ''
        carrera = ''

        if 'nivel_escolar' in request.POST:
            nivel_escolar = int(request.POST['nivel_escolar'])

        if 'carrera' in request.POST:
            carrera = request.POST['carrera']

        if nivel_escolar == 5 or nivel_escolar == 6:
            if carrera == '':
                form.add_error('carrera', 'Complete este campo.')

        if form.is_valid():
            licenciado_sma = form.save(commit=False)
            ci = licenciado_sma.ci
            licenciado_sma.edad = obtener_edad(ci)
            licenciado_sma.sexo = obtener_sexo(ci)
            if fecha_actual.month < 6:
                licenciado_sma.anno_entrevista = fecha_actual.year - 1
                licenciado_sma.mes_entrevista = 'Diciembre'
            elif 6 <= fecha_actual.month < 12:
                licenciado_sma.anno_entrevista = fecha_actual.year
                licenciado_sma.mes_entrevista = 'Junio'
            else:
                licenciado_sma.anno_entrevista = fecha_actual.year
                licenciado_sma.mes_entrevista = 'Diciembre'
            licenciado_sma.save()
            messages.add_message(request, messages.SUCCESS, "Registrado con éxito.")
            return redirect('/licenciados_sma')
        else:
            id_ubicacion = ''
            id_causa_no_aceptacion = ''
            id_acepto_oferta = ''
            id_recibio_oferta = ''
            id_carrera = ''
            id_nivel_escolar = ''
            if 'ubicacion' in request.POST:
                id_ubicacion = request.POST['ubicacion']
            if 'causa_no_aceptacion' in request.POST:
                id_causa_no_aceptacion = request.POST['causa_no_aceptacion']
            if 'acepto_oferta' in request.POST:
                id_acepto_oferta = request.POST['acepto_oferta']
            if 'recibio_oferta' in request.POST:
                id_recibio_oferta = request.POST['recibio_oferta']
            if 'nivel_escolar' in request.POST:
                id_nivel_escolar = request.POST['nivel_escolar']
            if 'carrera' in request.POST:
                id_carrera = request.POST['carrera']
            context = {'form_licenciados': form, 'nombre_form': "Registrar licenciado del SMA",
                       'carreras': carreras,'municipios': municipios,
                       'causa_no_acep': causa_no_acep, 'ubicaciones': ubicaciones,
                       'id_ubicacion': id_ubicacion,
                       'id_causa_no_aceptacion': id_causa_no_aceptacion, 'id_acepto_oferta': id_acepto_oferta,
                       'id_recibio_oferta': id_recibio_oferta, 'id_carrera': id_carrera,
                       'id_nivel_escolar': id_nivel_escolar, 'municipio_residencia': municipio_residencia}
            return render(request, "EmpleoEstatal/LicenciadosSMA/registrar_licenciado_sma.html", context)
    else:
        form = LicenciadosSMAForm()
    context = {'form_licenciados': form, 'nombre_form': "Registrar licenciado del SMA",
               'carreras': carreras,'municipios': municipios, 'municipio_residencia': municipio_residencia,
               'causa_no_acep': causa_no_acep, 'ubicaciones': ubicaciones}
    return render(request, "EmpleoEstatal/LicenciadosSMA/registrar_licenciado_sma.html", context)


@login_required
@permission_required(['administrador', 'dmt'])
def modificar_licenciado_sma(request, id_licenciado_sma):
    licenciado_sma = LicenciadosSMA.objects.get(id=id_licenciado_sma)

    if request.method == 'POST':
        form = LicenciadosSMAForm(request.POST, instance=licenciado_sma)

        recibio_oferta = ''
        acepto_oferta = ''
        ubicacion = ''

        if 'recibio_oferta' in request.POST:
            recibio_oferta = request.POST['recibio_oferta']
        if 'acepto_oferta' in request.POST:
            acepto_oferta = request.POST['acepto_oferta']
        if 'ubicacion' in request.POST:
            ubicacion = request.POST['ubicacion']

        if recibio_oferta and acepto_oferta == 'S' and ubicacion == '':
            form.add_error('ubicacion', 'Complete este campo.')

        nivel_escolar = ''
        carrera = ''

        if 'nivel_escolar' in request.POST:
            nivel_escolar = int(request.POST['nivel_escolar'])

        if 'carrera' in request.POST:
            carrera = request.POST['carrera']

        if nivel_escolar == 5 or nivel_escolar == 6:
            if carrera == '':
                form.add_error('carrera', 'Complete este campo.')

        if form.is_valid():
            ci = licenciado_sma.ci
            licenciado_sma.edad = obtener_edad(ci)
            licenciado_sma.sexo = obtener_sexo(ci)
            form.save()
            messages.add_message(request, messages.SUCCESS, "Modificado con éxito.")
            return redirect('/licenciados_sma')
        else:
            municipio_residencia = request.user.perfil_usuario.municipio
            causa_no_acep = CausalNoAceptacion.objects.filter(activo=True)
            ids_ubicaciones = [1, 2, 3, 4]
            ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
            municipios = Municipio.objects.all()
            errores = form.errors

            id_ubicacion = ''
            id_causa_no_aceptacion = ''
            id_acepto_oferta = ''
            id_recibio_oferta = ''
            id_carrera = ''
            id_nivel_escolar = ''
            id_municipio_entidad = ''
            if 'ubicacion' in request.POST:
                id_ubicacion = request.POST['ubicacion']
            if 'causa_no_aceptacion' in request.POST:
                id_causa_no_aceptacion = request.POST['causa_no_aceptacion']
            if 'acepto_oferta' in request.POST:
                id_acepto_oferta = request.POST['acepto_oferta']
            if 'recibio_oferta' in request.POST:
                id_recibio_oferta = request.POST['recibio_oferta']
            if 'nivel_escolar' in request.POST:
                id_nivel_escolar = request.POST['nivel_escolar']
            if 'carrera' in request.POST:
                id_carrera = request.POST['carrera']
            if 'municipio_entidad' in request.POST:
                id_municipio_entidad = request.POST['municipio_entidad']
            context = {'errores': errores, 'form_licenciados': form, 'nombre_form': "Registrar licenciado del SMA",
                       'municipios': municipios,
                       'causa_no_acep': causa_no_acep, 'ubicaciones': ubicaciones,
                       'id_municipio_entidad': id_municipio_entidad, 'id_ubicacion': id_ubicacion,
                       'id_causa_no_aceptacion': id_causa_no_aceptacion, 'id_acepto_oferta': id_acepto_oferta,
                       'id_recibio_oferta': id_recibio_oferta, 'id_carrera': id_carrera,
                       'id_nivel_escolar': id_nivel_escolar, 'municipio_residencia': municipio_residencia}
            return render(request, "EmpleoEstatal/LicenciadosSMA/modificar_licenciado_sma.html", context)
    else:
        form = LicenciadosSMAForm(instance=licenciado_sma)

    municipio_residencia = request.user.perfil_usuario.municipio
    causa_no_acep = CausalNoAceptacion.objects.filter(activo=True)
    ids_ubicaciones = [1, 2, 3, 4]
    ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
    municipios = Municipio.objects.all()
    errores = ''
    context = {'errores': errores, 'form_licenciados': form, 'licenciado_sma': licenciado_sma,
               'municipios': municipios, 'municipio_residencia': municipio_residencia,
               'causa_no_acep': causa_no_acep, 'ubicaciones': ubicaciones}
    return render(request, "EmpleoEstatal/LicenciadosSMA/modificar_licenciado_sma.html", context)


# REVISAR---REVISAR---REVISAR---REVISAR---REVISAR---REVISAR---REVISAR---REVISAR---REVISAR---REVISAR
@login_required
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def detalle_licenciado_sma(request, id_licenciado_sma):

    licenciado_sma = LicenciadosSMA.objects.get(id=id_licenciado_sma)
    controles = ControlLicenciadosSMA.objects.filter(licenciado_sma__id=id_licenciado_sma).order_by('id')
    c_licenciado_sma = controles.last()

    historiales = HistorialLicenciadosSMA.objects.filter(id_licenciado_sma=id_licenciado_sma)
    return render(request, "EmpleoEstatal/LicenciadosSMA/detalles_licenciado_sma.html", locals())


@login_required
@permission_required(['administrador', 'dmt'])
def dar_baja_licenciado_sma(request, id_licenciado_sma):
    licenciado_sma = LicenciadosSMA.objects.get(id=id_licenciado_sma)
    if request.method == 'POST':
        form = DarBajaLicenciadosSMAForm(request.POST, instance=licenciado_sma)
        if form.is_valid():
            id_causa = int(request.POST['causa_baja'])
            if id_causa == 5:
                licenciado_sma.delete()
            else:
                licenciado_sma.activo = False
                licenciado_sma.causa_baja = CausalBaja.objects.get(id=request.POST['causa_baja'])
                licenciado_sma.fecha_baja = datetime.datetime.now()
                form.save()
            messages.add_message(request, messages.SUCCESS, "El licenciado del sma ha sido dado de baja con éxito.")
            return redirect('/licenciados_sma')
    else:
        form = DarBajaLicenciadosSMAForm()
    context = {'form': form}
    return render(request, "EmpleoEstatal/LicenciadosSMA/dar_baja.html", context)


@login_required
@permission_required(['administrador'])
def re_incorporar_licenciado_sma(request, id_licenciado_sma):
    if request.method == 'POST':
        form = HistorialLicenciadoSMAForm(request.POST)
        if form.is_valid():
            historial_licenciado_sma= form.save(commit=False)
            historial_licenciado_sma.id_licenciado_sma = id_licenciado_sma
            historial_licenciado_sma.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Re-incorporado con éxito.")
            href = "/licenciados_sma/" + id_licenciado_sma
            return redirect(href)
    else:
        form = HistorialLicenciadoSMAForm()
    context = {'form': form, 'nombre_form': "Re-incorporar", 'id_licenciado_sma': id_licenciado_sma}
    return render(request, "EmpleoEstatal/LicenciadosSMA/re_incorporar.html", context)


@login_required
@permission_required(['administrador', 'dmt'])
def control_licenciado_sma(request, id_licenciado_sma):

    lic_sma = LicenciadosSMA.objects.get(id=id_licenciado_sma)

    ids_ubicaciones = [1, 2, 3, 4]
    ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
    organismos = Organismo.objects.filter(activo=True)
    municipios = Municipio.objects.all()

    if request.method == 'POST':
        form = ControlLicenciadosSMAForm(request.POST)
        if form.is_valid():
            c_licenciado_sma = form.save(commit=False)
            lic_sma.ubicacion = c_licenciado_sma.ubicacion
            if c_licenciado_sma.incorporado == 'S':
                lic_sma.fecha_ubicacion = datetime.datetime.now()
                lic_sma.incorporado = EstadoIncorporado.objects.get(id=1)
            else:
                lic_sma.incorporado = EstadoIncorporado.objects.get(id=2)

            c_licenciado_sma.licenciado_sma = lic_sma
            lic_sma.save()
            c_licenciado_sma.save()
            messages.add_message(request, messages.SUCCESS,
                                 "El control del licenciado del SMA ha sido registrado con éxito.")
            href = "/licenciados_sma/" + id_licenciado_sma
            return redirect(href)
    else:
        form = ControlLicenciadosSMAForm()

    context = {'form': form, 'nombre_form': "Registrar control del licenciado del SMA", 'municipios': municipios,
               'id_licenciado_sma': id_licenciado_sma, 'ubicaciones': ubicaciones, 'organismos': organismos}
    return render(request, "EmpleoEstatal/LicenciadosSMA/control_licenciado_sma.html", context)


@login_required
@permission_required(['administrador', 'dmt'])
def habilitar_licenciado_sma(request):

    print(LicenciadosSMA.objects.filter(activo=False, municipio_residencia__nombre='Bayamo').first().ci)

    ci = str(request.GET.get("ci", ""))
    errors = []
    context = {}

    if ci != "":
        try:
            busqueda = LicenciadosSMA.objects.filter(ci=ci)
            if busqueda.count() != 0:
                persona = busqueda.first()
                municipio_residencia = str(request.user.perfil_usuario.municipio.nombre)
                if str(persona.municipio_residencia.nombre) == municipio_residencia:
                    if not persona.activo:
                        persona.activo = True
                        persona.causa_baja = None
                        persona.fecha_baja = None
                        persona.save()

                        messages.add_message(request, messages.SUCCESS, "El licenciado del sma ha sido habilitado con éxito.")
                        return redirect('/licenciados_sma')
                    else:
                        errors.append("El licenciado del sma con CI {} ya se encuentra habilitado.".format(ci))
                else:
                    errors.append("CI {} pertenece al municipio {}.".format(ci, persona.municipio_residencia))
            else:
                errors.append("El licenciado del sma con CI {} no se encuentra registrado.".format(ci))

        except Exception as e:
            errors.append("Error. Vuelva a introducir el CI.")
            print("Error habilitando licenciado del SMA: {}, {}".format(e.args, e.message))

    context['ci'] = ci
    context['errors'] = errors
    return render(request, "EmpleoEstatal/LicenciadosSMA/habilitar_licenciado_sma.html", context)


@login_required
@permission_required(['administrador', 'dpt_ee', 'dmt'])
def reportes_licenciados_sma(request):
    return render(request, "EmpleoEstatal/LicenciadosSMA/Reportes/reportes_licenciados_sma.html")


@login_required
@permission_required(['administrador'])
def arreglar_errores(request):

    # No recibieron oferta
    lic = LicenciadosSMA.objects.filter(recibio_oferta=False, activo=True)
    for l in lic:
        l.recibio_oferta=True
        l.acepto_oferta='S'
        l.ubicacion = Ubicacion.objects.get(id=1)
        l.save()

    # Recibieron oferta, no la aceptaron y no tienen ubicacion
    lic = LicenciadosSMA.objects.filter(recibio_oferta=True, acepto_oferta='N', ubicacion=None, activo=True)
    for l in lic:
        l.ubicacion = Ubicacion.objects.get(id=1)
        l.save()

    # Recibio la oferta, acepto la oferta y no tiene ubicacion
    lic = LicenciadosSMA.objects.filter(recibio_oferta=True, acepto_oferta='S', ubicacion=None, activo=True)
    for l in lic:
        l.ubicacion = Ubicacion.objects.get(id=1)
        l.save()

    # Recibieron oferta y dejaron vacio el campo de aceptar la oferta
    lic = LicenciadosSMA.objects.filter(recibio_oferta=True, acepto_oferta='', activo=True)
    for l in lic:
        l.ubicacion = Ubicacion.objects.get(id=1)
        l.save()

    return redirect(listado_licenciados_sma)


def comprobar_pendientes(listado):

    causal_baja_automatica = CausalBaja.objects.get(id=10)
    fecha_actual = timezone.now()

    for persona in listado:
        persona.activo = False
        persona.causa_baja = causal_baja_automatica
        persona.fecha_baja = fecha_actual
        persona.save()


# PETICIONES AJAXS ---------------------------------------------------------------------------------------------------
from django.http import HttpResponse
from django.views.generic import TemplateView
import json


class PeticionAjaxSeleccionarCarreras(TemplateView):

    def get(self, request, *args, **kwargs):

        id_nivel_escolar = int(request.GET['id_nivel_escolar'])
        tipo = ''

        if id_nivel_escolar == 5:
            tipo = 'oc'
        if id_nivel_escolar == 6:
            tipo = 'nm'

        carreras = Carrera.objects.filter(tipo=tipo)

        carreras = [carreras_serializer(carrera) for carrera in carreras]
        return HttpResponse(json.dumps(carreras), content_type='application/json')


def carreras_serializer(carrera):
    return {'id_carrera': carrera.id, 'nombre_carrera': carrera.nombre}