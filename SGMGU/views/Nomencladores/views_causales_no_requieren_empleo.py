# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_causales_no_requieren_empleo(request):
    causales = CausalNoRequiereEmpleo.objects.all()
    return render(request, "Nomencladores/CausalesNoRequierenEmpleo/gestion_causales_no_requieren_empleo.html", locals())


@login_required
@permission_required(['administrador'])
def registrar_causal_no_requiere_empleo(request):
    if request.method == 'POST':
        form = CausalNoRequiereEmpleoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causa se ha registrado con éxito.")
            return redirect('/causales_no_requieren_empleo')
    else:
        form = CausalNoRequiereEmpleoForm()
    context = {'form': form, 'nombre_form': "Registrar: Causa"}
    return render(request, "Nomencladores/CausalesNoRequierenEmpleo/registrar_causal_no_requiere_empleo.html", context)


# @login_required
# @permission_required(['administrador'])
# def modificar_actividad_interrupto(request, id_actividad):
#     actividad = ActividadInterrupto.objects.get(id=id_actividad)
#     if request.method == 'POST':
#         form = ActividadInterruptoForm(request.POST, instance=actividad)
#         if form.is_valid():
#             form.save()
#             messages.add_message(request, messages.SUCCESS, "La actividad se ha modificado con éxito.")
#             return redirect('/actividades_interrupto')
#     else:
#         form = ActividadInterruptoForm(instance=actividad)
#     context = {'form': form, 'nombre_form': 'Modificar: Actividad'}
#     return render(request, "Nomencladores/ActividadInterrupto/modificar_actividad.html", context)
#
#
# @login_required
# @permission_required(['administrador'])
# def eliminar_actividad_interrupto(request, id_actividad):
#     actividad = ActividadInterrupto.objects.get(id=id_actividad)
#     actividad.activo = False
#     actividad.save()
#     messages.add_message(request, messages.SUCCESS, "La actividad se ha eliminado con éxito.")
#     return redirect('/actividades_interrupto')
