# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_causales_no_incorporacion(request):
    causales_no_incorporacion = CausalNoIncorporado.objects.all()
    return render(request, "CausalesNoIncorporacion/gestion_causales_no_incorporacion.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_causal_no_incorporacion(request):
    if request.method == 'POST':
        form = CausalNoIncorporacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causa de no incorporación se ha registrado con éxito.")
            return redirect('/causales_no_incorporacion')
    else:
        form = CausalNoIncorporacionForm()
    context = {'form': form, 'nombre_form': "Registrar Causa de no Incorporación"}
    return render(request, "CausalesNoIncorporacion/registrar_causal_no_incorporacion.html", context)


@login_required
@permission_required(['administrador'])
def modificar_causal_no_incorporacion(request, id_causal_no_incorporacion):
    causal_no_incorporacion = CausalNoIncorporado.objects.get(id=id_causal_no_incorporacion)
    if request.method == 'POST':
        form = CausalNoIncorporacionForm(request.POST, instance=causal_no_incorporacion)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causa de no incorporación se ha modificado con éxito.")
            return redirect('/causales_no_incorporacion')
    else:
        form = CausalNoIncorporacionForm(instance=causal_no_incorporacion)
    context = {'form': form}
    return render(request, "CausalesNoIncorporacion/modificar_causal_no_incorporacion.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_causal_no_incorporacion(request, id_causal_no_incorporacion):
    causal_no_incorporacion = CausalNoIncorporado.objects.get(id=id_causal_no_incorporacion)
    causal_no_incorporacion.activo = False
    causal_no_incorporacion.save()
    messages.add_message(request, messages.SUCCESS, "La causa de no incorporación se ha eliminado con éxito.")
    return redirect('/causales_no_incorporacion')


# @login_required
# @permission_required(['administrador'])
# def activar_nivel_escolar(request, id_nivel_escolar):
#     nivel_escolar = NivelEscolar.objects.get(id=id_nivel_escolar)
#     nivel_escolar.activo = True
#     nivel_escolar.save()
#     messages.add_message(request, messages.SUCCESS, "El nivel escolar se ha activado con éxito.")
#     return redirect('/niveles_escolares')
