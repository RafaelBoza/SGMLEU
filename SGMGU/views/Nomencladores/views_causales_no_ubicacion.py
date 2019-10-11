# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_causales_no_ubicacion(administrador):
    causales_no_ubicacion = CausalNoUbicado.objects.all()
    return render(administrador, "CausalesNoUbicacion/gestion_causales_no_ubicacion.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_causal_no_ubicacion(administrador):
    if administrador.method == 'POST':
        form = CausalNoUbicacionForm(administrador.POST)
        if form.is_valid():
            form.save()
            messages.add_message(administrador, messages.SUCCESS, "La causa de no ubicación se ha registrado con éxito.")
            return redirect('/causales_no_ubicacion')
    else:
        form = CausalNoUbicacionForm()
    context = {'form': form, 'nombre_form': "Registrar Causa de no Ubicación"}
    return render(administrador, "CausalesNoUbicacion/registrar_causal_no_ubicacion.html", context)


@login_required
@permission_required(['administrador'])
def modificar_causal_no_ubicacion(administrador, id_causal_no_ubicacion):
    causal_no_ubicacion = CausalNoUbicado.objects.get(id=id_causal_no_ubicacion)
    if administrador.method == 'POST':
        form = CausalNoUbicacionForm(administrador.POST, instance=causal_no_ubicacion)
        if form.is_valid():
            form.save()
            messages.add_message(administrador, messages.SUCCESS, "La causa de no ubicación se ha modificado con éxito.")
            return redirect('/causales_no_ubicacion')
    else:
        form = CausalNoUbicacionForm(instance=causal_no_ubicacion)
    context = {'form': form}
    return render(administrador, "CausalesNoUbicacion/modificar_causal_no_ubicacion.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_causal_no_ubicacion(administrador, id_causal_no_ubicacion):
    causal_no_ubicacion = CausalNoUbicado.objects.get(id=id_causal_no_ubicacion)
    causal_no_ubicacion.activo = False
    causal_no_ubicacion.save()
    messages.add_message(administrador, messages.SUCCESS, "La causa de no ubicación se ha eliminado con éxito.")
    return redirect('/causales_no_ubicacion')


# @login_required
# @permission_required(['administrador'])
# def activar_nivel_escolar(administrador, id_nivel_escolar):
#     nivel_escolar = NivelEscolar.objects.get(id=id_nivel_escolar)
#     nivel_escolar.activo = True
#     nivel_escolar.save()
#     messages.add_message(administrador, messages.SUCCESS, "El nivel escolar se ha activado con éxito.")
#     return redirect('/niveles_escolares')
