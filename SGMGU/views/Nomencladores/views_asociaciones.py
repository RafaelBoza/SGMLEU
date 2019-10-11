# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_asociaciones(request):
    asociaciones = Asociacion.objects.all()
    return render(request, "Nomencladores/Asociaciones/gestion_asociaciones.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_asociacion(request):
    if request.method == 'POST':
        form = AsociacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La asociación se ha registrado con éxito.")
            return redirect('/asociaciones')
    else:
        form = AsociacionForm()
    context = {'form': form, 'nombre_form': "Registrar Asociación"}
    return render(request, "Nomencladores/Asociaciones/registrar_asociacion.html", context)


@login_required
@permission_required(['administrador'])
def modificar_asociacion(request, id_asociacion):
    asociacion = Asociacion.objects.get(id=id_asociacion)
    if request.method == 'POST':
        form = AsociacionForm(request.POST, instance=asociacion)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La asociación se ha modificado con éxito.")
            return redirect('/asociaciones')
    else:
        form = AsociacionForm(instance=asociacion)
    context = {'form': form}
    return render(request, "Nomencladores/Asociaciones/modificar_asociacion.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_asociacion(request, id_asociacion):
    asociaciones = Asociacion.objects.get(id=id_asociacion)
    asociaciones.activo = False
    asociaciones.save()
    messages.add_message(request, messages.SUCCESS, "La asociación se ha eliminado con éxito.")
    return redirect('/asociaciones')
