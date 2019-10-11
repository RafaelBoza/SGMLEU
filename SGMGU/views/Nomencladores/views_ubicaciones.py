# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_ubicaciones(request):
    ubicaciones = Ubicacion.objects.all()
    return render(request, "Ubicacion/gestion_ubicacion.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_ub(request):
    if request.method == 'POST':
        form = UbicacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La ubicación se ha registrado con éxito.")
            return redirect('/ubicaciones')
    else:
        form = UbicacionForm()
    context = {'form': form, 'nombre_form': "Registrar Ubicación"}
    return render(request, "Ubicacion/registrar_ubicacion.html", context)


@login_required
@permission_required(['administrador'])
def modificar_ubicacion(request, id_ubicacion):
    ubicacion = Ubicacion.objects.get(id=id_ubicacion)
    if request.method == 'POST':
        form = UbicacionForm(request.POST, instance=ubicacion)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La ubicación se ha modificado con éxito.")
            return redirect('/ubicaciones')
    else:
        form = UbicacionForm(instance=ubicacion)
    context = {'form': form}
    return render(request, "Ubicacion/modificar_ubicacion.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_ubicacion(request, id_ubicacion):
    ubicacion = Ubicacion.objects.get(id=id_ubicacion)
    ubicacion.activo = False
    ubicacion.save()
    messages.add_message(request, messages.SUCCESS, "La ubicación se ha eliminado con éxito.")
    return redirect('/ubicaciones')
