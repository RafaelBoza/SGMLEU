# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_delitos(request):
    delitos = Delito.objects.all()
    return render(request, "Delitos/gestion_delitos.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_delito(request):
    if request.method == 'POST':
        form = DelitoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El delito se ha registrado con éxito.")
            return redirect('/delitos')
    else:
        form = DelitoForm()
    context = {'form': form, 'nombre_form': "Registrar Delito"}
    return render(request, "Delitos/registrar_delitos.html", context)


@login_required
@permission_required(['administrador'])
def modificar_delito(request, id_delito):
    delito = Delito.objects.get(id=id_delito)
    if request.method == 'POST':
        form = DelitoForm(request.POST, instance=delito)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El delito se ha modificado con éxito.")
            return redirect('/delitos')
    else:
        form = DelitoForm(instance=delito)
    context = {'form': form}
    return render(request, "Delitos/modificar_delitos.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_delito(request, id_delito):
    delitos = Delito.objects.get(id=id_delito)
    delitos.activo = False
    delitos.save()
    messages.add_message(request, messages.SUCCESS, "El delito se ha eliminado con éxito.")
    return redirect('/delitos')