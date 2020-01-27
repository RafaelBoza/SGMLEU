# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import get_object_or_404
import xml.etree.ElementTree as ET
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from SGMGU.views.utiles import *
import datetime
from django.db.models import Q
from django.http import HttpResponse
import xlrd


@login_required()
@permission_required(['administrador', 'trabajador_social_joven_abandona', 'universidad_joven_abandona', 'dmt_joven_abandona', 'dpt_ee'])
def gestion_jovenes_abandonan_nivel_superior(request):

    perfil_usuario = request.user.perfil_usuario
    centro_estudio = perfil_usuario.universidad
    provincia = perfil_usuario.provincia
    municipio = perfil_usuario.municipio
    categoria = perfil_usuario.categoria.nombre
    fecha_actual = datetime.datetime.today()

    q = request.GET.get("q")

    if categoria == 'universidad_joven_abandona':
        jovenes = JovenAbandonanNS.objects.filter(centro_estudio=centro_estudio). \
            values('id', 'nombre_apellidos', 'ci', 'municipio_residencia__nombre', 'carrera_abandona__nombre', 'activo')
        if q:
            jovenes = jovenes.filter(
                Q(nombre_apellidos__icontains=q) |
                Q(ci__icontains=q)
            )

    elif categoria == 'trabajador_social_joven_abandona'or categoria == 'dmt_joven_abandona':
        jovenes = JovenAbandonanNS.objects.filter(municipio_residencia=municipio). \
            values('id', 'nombre_apellidos', 'ci', 'municipio_residencia__nombre', 'carrera_abandona__nombre', 'activo')
        if q:
            jovenes = jovenes.filter(
                Q(nombre_apellidos__icontains=q) |
                Q(ci__icontains=q)
            )

    elif categoria == 'dpt_ee':
        jovenes = JovenAbandonanNS.objects.filter(municipio_residencia__provincia=provincia). \
            values('id', 'nombre_apellidos', 'ci', 'municipio_residencia__nombre', 'carrera_abandona__nombre', 'activo')
        if q:
            jovenes = jovenes.filter(
                Q(nombre_apellidos__icontains=q) |
                Q(ci__icontains=q)
            )

    elif categoria == 'administrador':
        jovenes = JovenAbandonanNS.objects.all(). \
            values('id', 'nombre_apellidos', 'ci', 'municipio_residencia__nombre', 'carrera_abandona__nombre', 'activo')
        if q:
            jovenes = jovenes.filter(
                Q(nombre_apellidos__icontains=q) |
                Q(ci__icontains=q)
            )
    else:
        return redirect('/logout')

    jovenes = paginar(request, jovenes)
    paginas = crear_lista_pages(jovenes)

    context = {
        'jovenes': jovenes,
        'paginas': paginas,
        'categoria': categoria,
        'nombre_pag': 'Seguimiento a jóvenes que abandonan la enseñanza en el nivel superior'
    }

    return render(request, "JovenesAbandonanNS/gestion_jovenes_abandonan_nivel_superior.html", context)


@login_required()
@permission_required(['administrador', 'universidad_joven_abandona'])
def registrar_joven_abandona_nivel_superior(request):

    if request.method == 'POST':
        form = JovenAbandonanNSForm(request.POST)

        if form.is_valid():
            joven_abandona = form.save(commit=False)
            joven_abandona.save()

            messages.add_message(request, messages.SUCCESS, "Registrado con éxito.")

            return redirect('/seguimiento_jovenes_abandonan_nivel_superior')
        else:

            context = {
                'form': form,
                'nombre_form': "Registrar: Interrupto"
            }

            return render(request, "JovenesAbandonanNS/registrar_modificar_joven_abandona_ns.html", context)
    else:
        form = JovenAbandonanNSForm()

    context = {
        'form': form,
        'nombre_form': "Registrar:"
    }

    return render(request, "JovenesAbandonanNS/registrar_modificar_joven_abandona_ns.html", context)


@login_required()
@permission_required(['administrador', 'universidad_joven_abandona'])
def modificar_joven_abandona_nivel_superior(request, id_joven):

    joven_abandona = JovenAbandonanNS.objects.get(id=id_joven)

    if request.method == 'POST':
        form = JovenAbandonanNSForm(request.POST, instance=joven_abandona)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Modificado con éxito.")
            return redirect('/seguimiento_jovenes_abandonan_nivel_superior')
        else:
            context = {'form': form}
            return render(request, "JovenesAbandonanNS/registrar_modificar_joven_abandona_ns.html", context)
    else:
        form = JovenAbandonanNSForm(instance=joven_abandona)

    context = {'form': form}
    return render(request, "JovenesAbandonanNS/registrar_modificar_joven_abandona_ns.html", context)


@login_required()
@permission_required(['administrador', 'trabajador_social_joven_abandona'])
def proceso_trabajador_social_jans(request, id_joven):

    if request.method == 'POST':
        form = ProcesoTrabajadorSocialJANSForm(request.POST)

        if form.is_valid():
            proceso_ts_joven_abandona = form.save(commit=False)
            proceso_ts_joven_abandona.joven_abandona = JovenAbandonanNS.objects.get(id=id_joven)
            proceso_ts_joven_abandona.save()

            messages.add_message(request, messages.SUCCESS, "Proceso finalizado con éxito.")

            return redirect('/seguimiento_jovenes_abandonan_nivel_superior/{}'.format(id_joven))
        else:

            context = {
                'form': form,
                'nombre_form': "Proceso realizado por el trabajo social",
                "id_joven": id_joven
            }

            return render(request, "JovenesAbandonanNS/proceso_trabajador_social_jans.html", context)
    else:
        form = ProcesoTrabajadorSocialJANSForm()

    context = {
        'form': form,
        'nombre_form': "Proceso realizado por el trabajo social",
        "id_joven": id_joven
    }

    return render(request, "JovenesAbandonanNS/proceso_trabajador_social_jans.html", context)


@login_required()
@permission_required(['administrador', 'dmt_joven_abandona'])
def proceso_direccion_empleo_jans(request, id_joven):

    ids_ubicaciones = [1, 2, 3, 4]
    ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
    organismos = Organismo.objects.filter(activo=True)
    municipios = Municipio.objects.all()

    if request.method == 'POST':
        form = ProcesoDireccionMEmpleoJANSForm(request.POST)

        if form.is_valid():
            proceso_dmt_joven_abandona = form.save(commit=False)
            proceso_dmt_joven_abandona.joven_abandona = JovenAbandonanNS.objects.get(id=id_joven)
            proceso_dmt_joven_abandona.save()

            messages.add_message(request, messages.SUCCESS, "Proceso finalizado con éxito.")

            return redirect('/seguimiento_jovenes_abandonan_nivel_superior/{}'.format(id_joven))
        else:

            context = {
                'form': form,
                'nombre_form': "Proceso realizado por la dirección de empleo",
                "id_joven": id_joven,
                'ubicaciones': ubicaciones,
                'organismos': organismos,
                'municipios': municipios
            }

            return render(request, "JovenesAbandonanNS/proceso_direccion_empleo_jans.html", context)
    else:
        form = ProcesoDireccionMEmpleoJANSForm()

    context = {
        'form': form,
        'nombre_form': "Proceso realizado por la dirección de empleo",
        "id_joven": id_joven,
        'ubicaciones': ubicaciones,
        'organismos': organismos,
        'municipios': municipios
    }

    return render(request, "JovenesAbandonanNS/proceso_direccion_empleo_jans.html", context)


@login_required()
@permission_required(['administrador', 'dmt_joven_abandona'])
def proceso_control_jans(request, id_joven):

    ids_ubicaciones = [1, 2, 3, 4]
    ubicaciones = Ubicacion.objects.filter(activo=True, id__in=ids_ubicaciones)
    organismos = Organismo.objects.filter(activo=True)
    municipios = Municipio.objects.all()

    if request.method == 'POST':
        form = ControlJovenAbandonanNSForm(request.POST)

        if form.is_valid():
            proceso_control_abandona = form.save(commit=False)
            proceso_control_abandona.joven_abandona = JovenAbandonanNS.objects.get(id=id_joven)
            proceso_control_abandona.save()

            messages.add_message(request, messages.SUCCESS, "Proceso finalizado con éxito.")

            return redirect('/seguimiento_jovenes_abandonan_nivel_superior/{}'.format(id_joven))
        else:

            context = {
                'form': form,
                'nombre_form': "Control realizado por la dirección de empleo",
                "id_joven": id_joven,
                'ubicaciones': ubicaciones,
                'organismos': organismos,
                'municipios': municipios
            }

            return render(request, "JovenesAbandonanNS/proceso_control_jans.html", context)
    else:
        form = ControlJovenAbandonanNSForm()

    context = {
        'form': form,
        'nombre_form': "Control realizado por la dirección de empleo",
        "id_joven": id_joven,
        'ubicaciones': ubicaciones,
        'organismos': organismos,
        'municipios': municipios
    }

    return render(request, "JovenesAbandonanNS/proceso_control_jans.html", context)



@login_required()
@permission_required(['administrador', 'trabajador_social_joven_abandona', 'universidad_joven_abandona', 'dmt_joven_abandona', 'dpt_ee'])
def detalles_joven_abandona_nivel_superior(request, id_joven):

    categoria = request.user.perfil_usuario.categoria.nombre
    joven_abandona = get_object_or_404(JovenAbandonanNS, id=id_joven)

    proceso_realizado_trabajador_social = ProcesoTrabajadorSocialJANS.objects.filter(joven_abandona=id_joven)

    proceso_realizado_direccion_m_empleo = ProcesoDireccionMEmpleoJANS.objects.filter(joven_abandona=id_joven)

    control_realizado_direccion_m_empleo = ControlJovenAbandonanNS.objects.filter(joven_abandona=id_joven)

    context = {
        'joven_abandona': joven_abandona,
        'nombre_pag': "Datos del Joven: {}".format(joven_abandona.nombre_apellidos),
        'edad': obtener_edad(joven_abandona.ci),
        'categoria': categoria,
        'proceso_realizado_trabajador_social': proceso_realizado_trabajador_social,
        'proceso_realizado_direccion_m_empleo': proceso_realizado_direccion_m_empleo,
        'control_realizado_direccion_m_empleo': control_realizado_direccion_m_empleo,
    }

    return render(request, "JovenesAbandonanNS/detalles_joven_abandona_ns.html", context)


@login_required()
@permission_required(['administrador'])
def eliminar_joven_abandona_nivel_superior(request, id_joven):

    joven = JovenAbandonanNS.objects.get(id=id_joven)
    joven.delete()
    messages.add_message(request, messages.SUCCESS, "Eliminado con éxito.")

    return redirect('/seguimiento_jovenes_abandonan_nivel_superior')


@login_required()
@permission_required(['administrador'])
def activar_joven_abandona_nivel_superior(request, id_joven):

    joven = JovenAbandonanNS.objects.get(id=id_joven)
    joven.activo = True
    messages.add_message(request, messages.SUCCESS, "Activado con éxito.")

    return redirect('/seguimiento_jovenes_abandonan_nivel_superior')


@login_required()
@permission_required(['administrador'])
def desactivar_joven_abandona_nivel_superior(request, id_joven):

    joven = JovenAbandonanNS.objects.get(id=id_joven)
    joven.activo = False
    messages.add_message(request, messages.SUCCESS, "Desactivado con éxito.")

    return redirect('/seguimiento_jovenes_abandonan_nivel_superior')


@login_required
@permission_required(['administrador', 'universidad_joven_abandona'])
def importar_jovenes_abandonan(request):

    if request.method == 'POST':
        errors = []
        xml_file = request.FILES['jovenes_abandonan_file']

        if xml_file.name.split(".")[-1] != 'xml':
            messages.add_message(request, messages.ERROR, "El archivo subido es incorrecto")
            return redirect('/seguimiento_jovenes_abandonan_nivel_superior')
        else:
            book = ET.parse(xml_file).getroot()
            print(book)

            #                                        #
            # AQUI VA EL CODIGO PARA PARSEAR EL XML  #
            #                                        #

        if len(errors) > 0:
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = "attachment; filename=Errores_encontrados_al_importar_jovenes_que_abandonan.xlsx"
            book = Workbook(response, {'in_memory': True})
            bold = book.add_format({'bold': True, 'border': 1})
            format = book.add_format({'border': 1})
            sheet = book.add_worksheet("Errores")

            sheet.set_column('A:A', 10)
            sheet.set_column('B:B', 80)
            sheet.write(0, 0,  "No.Fila",bold)
            sheet.write(0, 1,  "Error",bold)

            for i, error in enumerate(errors):
                sheet.write(i + 1, 0, unicode(error[0]), format)
                sheet.write(i + 1, 1, error[1].decode('utf-8'), format)
            book.close()
            messages.add_message(request, messages.SUCCESS, "XML importado.   NOTA: Ocurrieron algunos errores al importar el XML.")
            return response
        else:
            messages.add_message(request, messages.SUCCESS, "XML importado con éxito.")
            return redirect("/seguimiento_jovenes_abandonan_nivel_superior")
