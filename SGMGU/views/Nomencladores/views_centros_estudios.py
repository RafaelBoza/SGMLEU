# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_centros_estudios(request):
    centros_estudios=Centro_estudio.objects.all()
    context = {'centros_estudios': centros_estudios}
    return render(request, "CentroEstudios/gestion_centro_estudios.html", context)

@login_required
@permission_required(['administrador'])
def registrar_centro_estudios(request):
    if request.method == 'POST':
        form=RegistrarCentroEstudioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El centro de estudios se ha registrado con éxito.")
            return redirect('/centros_estudios')
    else:
        form = RegistrarCentroEstudioForm()
    context = {'form':form}
    return render(request, "CentroEstudios/registrar_centro_estudio.html", context)


@login_required
@permission_required(['administrador'])
def modificar_centro_estudios(request,id_centro_estudio):
    centro_estudios=Centro_estudio.objects.get(id=id_centro_estudio)
    if request.method == 'POST':
        form=RegistrarCentroEstudioForm(request.POST,instance=centro_estudios)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El centro de estudios se ha modificado con éxito.")
            return redirect('/centros_estudios')
    else:
        form = RegistrarCentroEstudioForm(instance=centro_estudios)
    # Creamos el contexto
    context = {'form':form}
    # Y mostramos los datos
    return render(request, "CentroEstudios/modificar_centro_estudio.html", context)



@login_required
@permission_required(['administrador'])
def eliminar_centro_estudios(request,id_centro_estudio):
    centro_estudios=Centro_estudio.objects.get(id=id_centro_estudio)
    centro_estudios.activo=False
    centro_estudios.save()
    messages.add_message(request, messages.SUCCESS, "El centro de estudios se ha eliminado con éxito.")
    return redirect('/centros_estudios')
