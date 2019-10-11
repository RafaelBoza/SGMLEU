# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_niveles_escolares(request):
    niveles_escolares = NivelEscolar.objects.all()
    return render(request, "NivelesEscolares/gestion_niveles_escolares.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_nivel_escolar(request):
    if request.method == 'POST':
        form = NivelEscolarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El nivel escolar se ha registrado con éxito.")
            return redirect('/niveles_escolares')
    else:
        form = NivelEscolarForm()
    context = {'form': form, 'nombre_form': "Registrar Nivlel Escolar"}
    return render(request, "NivelesEscolares/registrar_nivel_escolar.html", context)


@login_required
@permission_required(['administrador'])
def modificar_nivelel_escolar(request, id_nivel_escolar):
    nivel_escolar = NivelEscolar.objects.get(id=id_nivel_escolar)
    if request.method == 'POST':
        form = NivelEscolarForm(request.POST, instance=nivel_escolar)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El nivel escolar se ha modificado con éxito.")
            return redirect('/niveles_escolares')
    else:
        form = NivelEscolarForm(instance=nivel_escolar)
    context = {'form': form}
    return render(request, "NivelesEscolares/modificar_nivel_escolar.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_nivel_escolar(request, id_nivel_escolar):
    nivel_escolar = NivelEscolar.objects.get(id=id_nivel_escolar)
    nivel_escolar.activo = False
    nivel_escolar.save()
    messages.add_message(request, messages.SUCCESS, "El nivel escolar se ha eliminado con éxito.")
    return redirect('/niveles_escolares')


# @login_required
# @permission_required(['administrador'])
# def activar_nivel_escolar(request, id_nivel_escolar):
#     nivel_escolar = NivelEscolar.objects.get(id=id_nivel_escolar)
#     nivel_escolar.activo = True
#     nivel_escolar.save()
#     messages.add_message(request, messages.SUCCESS, "El nivel escolar se ha activado con éxito.")
#     return redirect('/niveles_escolares')
