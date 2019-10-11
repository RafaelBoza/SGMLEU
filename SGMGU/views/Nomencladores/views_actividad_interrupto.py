# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_actividades_interrupto(request):
    actividades = ActividadInterrupto.objects.all()
    return render(request, "Nomencladores/ActividadInterrupto/gestion_actividades.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_actividad_interrupto(request):
    if request.method == 'POST':
        form = ActividadInterruptoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La actividad se ha registrado con éxito.")
            return redirect('/actividades_interrupto')
    else:
        form = ActividadInterruptoForm()
    context = {'form': form, 'nombre_form': "Registrar: Actividad"}
    return render(request, "Nomencladores/ActividadInterrupto/registrar_actividad.html", context)


@login_required
@permission_required(['administrador'])
def modificar_actividad_interrupto(request, id_actividad):
    actividad = ActividadInterrupto.objects.get(id=id_actividad)
    if request.method == 'POST':
        form = ActividadInterruptoForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La actividad se ha modificado con éxito.")
            return redirect('/actividades_interrupto')
    else:
        form = ActividadInterruptoForm(instance=actividad)
    context = {'form': form, 'nombre_form': 'Modificar: Actividad'}
    return render(request, "Nomencladores/ActividadInterrupto/modificar_actividad.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_actividad_interrupto(request, id_actividad):
    actividad = ActividadInterrupto.objects.get(id=id_actividad)
    actividad.activo = False
    actividad.save()
    messages.add_message(request, messages.SUCCESS, "La actividad se ha eliminado con éxito.")
    return redirect('/actividades_interrupto')
