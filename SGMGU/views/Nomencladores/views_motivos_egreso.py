# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_motivos_egreso(request):
    motivos_egreso = MotivoEgreso.objects.all()
    return render(request, "MotivoEgreso/gestion_motivos_egreso.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_motivo_egreso(request):
    if request.method == 'POST':
        form = MotivoEgresoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El motivo de egreso se ha registrado con éxito.")
            return redirect('/motivos_egreso')
    else:
        form = MotivoEgresoForm()
    context = {'form': form, 'nombre_form': "Motivo de Egreso"}
    return render(request, "MotivoEgreso/registrar_motivo_egreso.html", context)


@login_required
@permission_required(['administrador'])
def modificar_motivo_egreso(request, id_motivo_egreso):
    motivo_egreso = MotivoEgreso.objects.get(id=id_motivo_egreso)
    if request.method == 'POST':
        form = MotivoEgresoForm(request.POST, instance=motivo_egreso)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El motivo de egreso se ha modificado con éxito.")
            return redirect('/motivos_egreso')
    else:
        form = MotivoEgresoForm(instance=motivo_egreso)
    context = {'form': form}
    return render(request, "MotivoEgreso/modificar_motivo_egreso.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_motivo_egreso(request, id_motivo_egreso):
    motivo_egreso = MotivoEgreso.objects.get(id=id_motivo_egreso)
    motivo_egreso.activo = False
    motivo_egreso.save()
    messages.add_message(request, messages.SUCCESS, "El motivo de egreso se ha eliminado con éxito.")
    return redirect('/motivos_egreso')
