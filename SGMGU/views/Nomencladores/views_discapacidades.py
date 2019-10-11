# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_discapacidades(request):
    discapacidades = Discapacidad.objects.all()
    return render(request, "Nomencladores/Discapacidades/gestion_discapacidades.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_discapacidad(request):
    if request.method == 'POST':
        form = DiscapacidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La discapacidad se ha registrado con éxito.")
            return redirect('/discapacidades')
    else:
        form = DiscapacidadForm()
    context = {'form': form, 'nombre_form': "Registrar Discapacidad"}
    return render(request, "Nomencladores/Discapacidades/registrar_discapacidad.html", context)


@login_required
@permission_required(['administrador'])
def modificar_discapacidad(request, id_discapacidad):
    discapacidad = Discapacidad.objects.get(id=id_discapacidad)
    if request.method == 'POST':
        form = DiscapacidadForm(request.POST, instance=discapacidad)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La discapacidad se ha modificado con éxito.")
            return redirect('/discapacidades')
    else:
        form = DiscapacidadForm(instance=discapacidad)
    context = {'form': form}
    return render(request, "Nomencladores/Discapacidades/modificar_discapacidad.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_discapacidad(request, id_discapacidad):
    discapacidad = Discapacidad.objects.get(id=id_discapacidad)
    discapacidad.activo = False
    discapacidad.save()
    messages.add_message(request, messages.SUCCESS, "La discapacidad se ha eliminado con éxito.")
    return redirect('/discapacidades')
