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

    ci = str(request.GET.get("ci", ""))
    errors = []
    context = {}

    if ci != "":
        try:
            busqueda = LicenciadosSMA.objects.filter(ci=ci)
            if busqueda.count() != 0:
                persona = busqueda.first()
                if request.user.perfil_usuario.categoria.nombre == 'administrador' or \
                        str(persona.municipio_residencia.nombre.encode('utf-8').strip()) == str(request.user.perfil_usuario.municipio.nombre.encode('utf-8').strip()):
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
                    errors.append("CI {} pertenece al municipio {}.".format(ci, str(persona.municipio_residencia.nombre.encode('utf-8').strip())))
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