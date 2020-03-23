# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador'])
def gestion_causales_desvinculacion_ns(request):
    causales = CausalDesvinculacionNS.objects.all()
    context = {'causales': causales}
    return render(request, "Nomencladores/CausalDesvinculacionNS/gestion_causales_desvinculacion_ns.html", context)

@login_required
@permission_required(['administrador'])
def registrar_causal_desvinculacion_ns(request):
    if request.method == 'POST':
        form = CausalDesvinculacionNSForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causa de desvinculación se ha registrado con éxito.")
            return redirect('/causales_desvinculacion_ns')
    else:
        form = CausalDesvinculacionNSForm()
    context = {'form': form}
    return render(request, "Nomencladores/CausalDesvinculacionNS/registrar_causal_desvinculacion_ns.html", context)


@login_required
@permission_required(['administrador'])
def modificar_causal_desvinculacion_ns(request, id_causal_desvinculacion_ns):
    causal_desvinculacion_ns = CausalDesvinculacionNS.objects.get(id=id_causal_desvinculacion_ns)
    if request.method == 'POST':
        form = CausalDesvinculacionNSForm(request.POST, instance=causal_desvinculacion_ns)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causa de desvinculación se ha modificado con éxito.")
            return redirect('/causales_desvinculacion_ns')
    else:
        form = CausalDesvinculacionNSForm(instance=causal_desvinculacion_ns)
    context = {'form': form}
    return render(request, "Nomencladores/CausalDesvinculacionNS/modifical_causal_desvinculacion_ns.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_causal_desvinculacion_ns(request, id_causal_desvinculacion_ns):
    causal_desvinculacion_ns = CausalDesvinculacionNS.objects.get(id=id_causal_desvinculacion_ns)
    causal_desvinculacion_ns.activo = False
    causal_desvinculacion_ns.save()
    messages.add_message(request, messages.SUCCESS, "La causa de desvinculación se ha eliminado con éxito.")
    return redirect('/causales_desvinculacion_ns')
