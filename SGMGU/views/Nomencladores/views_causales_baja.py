# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_causales_baja(request):
    causales_baja = CausalBaja.objects.all()
    return render(request, "CausalesBaja/gestion_causales_baja.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_causal_baja(request):
    if request.method == 'POST':
        form = CausalBajaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causa de baja se ha registrado con éxito.")
            return redirect('/causales_baja')
    else:
        form = CausalBajaForm()
    context = {'form': form, 'nombre_form': "Registrar Causa de Baja"}
    return render(request, "CausalesBaja/registrar_causal_baja.html", context)


@login_required
@permission_required(['administrador'])
def modificar_causal_baja(request, id_causal_baja):
    causal_baja = CausalBaja.objects.get(id=id_causal_baja)
    if request.method == 'POST':
        form = CausalBajaForm(request.POST, instance=causal_baja)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causa de baja se ha modificado con éxito.")
            return redirect('/causales_baja')
    else:
        form = CausalBajaForm(instance=causal_baja)
    context = {'form': form}
    return render(request, "CausalesBaja/modificar_causal_baja.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_causal_baja(request, id_causal_baja):
    causal_baja = CausalBaja.objects.get(id=id_causal_baja)
    causal_baja.activo = False
    causal_baja.save()
    messages.add_message(request, messages.SUCCESS, "La causa de baja se ha eliminado con éxito.")
    return redirect('/causales_baja')


# @login_required
# @permission_required(['administrador'])
# def activar_nivel_escolar(request, id_nivel_escolar):
#     nivel_escolar = NivelEscolar.objects.get(id=id_nivel_escolar)
#     nivel_escolar.activo = True
#     nivel_escolar.save()
#     messages.add_message(request, messages.SUCCESS, "El nivel escolar se ha activado con éxito.")
#     return redirect('/niveles_escolares')
