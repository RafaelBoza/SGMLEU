# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_estados_incorporados(request):
    estados_incorporados = EstadoIncorporado.objects.all()
    return render(request, "EstadoIncorporado/gestion_estado_incorporado.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_estado_incorporado(request):
    if request.method == 'POST':
        form = EstadoIncorporadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El estado se ha registrado con éxito.")
            return redirect('/estados_incorporados')
    else:
        form = EstadoIncorporadoForm()
    context = {'form': form, 'nombre_form': "Registrar Estado de Incorporado"}
    return render(request, "EstadoIncorporado/registrar_estado_incorporado.html", context)


@login_required
@permission_required(['administrador'])
def modificar_estado_incorporado(request, id_estado_incorporado):
    estado_incorporado = EstadoIncorporado.objects.get(id=id_estado_incorporado)
    if request.method == 'POST':
        form = EstadoIncorporadoForm(request.POST, instance=estado_incorporado)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El estado se ha modificado con éxito.")
            return redirect('/estados_incorporados')
    else:
        form = EstadoIncorporadoForm(instance=estado_incorporado)
    context = {'form': form}
    return render(request, "EstadoIncorporado/modificar_estado_incorporado.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_estado_incorporado(request, id_estado_incorporado):
    estado_incorporado = EstadoIncorporado.objects.get(id=id_estado_incorporado)
    estado_incorporado.activo = False
    estado_incorporado.save()
    messages.add_message(request, messages.SUCCESS, "El estado se ha eliminado con éxito.")
    return redirect('/estados_incorporados')


# @login_required
# @permission_required(['administrador'])
# def activar_nivel_escolar(request, id_nivel_escolar):
#     nivel_escolar = NivelEscolar.objects.get(id=id_nivel_escolar)
#     nivel_escolar.activo = True
#     nivel_escolar.save()
#     messages.add_message(request, messages.SUCCESS, "El nivel escolar se ha activado con éxito.")
#     return redirect('/niveles_escolares')
