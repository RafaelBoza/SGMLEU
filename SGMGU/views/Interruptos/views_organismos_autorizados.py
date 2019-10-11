# -*- coding: utf-8 -*-
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from SGMGU.views.utiles import *


@login_required
@permission_required(['administrador', 'especialista'])
def gestion_organismos_autorizados(request):

    organismos_autorizados = OrganismosAutorizadosRegistrarInterrupto.objects.all()
    if organismos_autorizados.count() > 0:
        for organismo in organismos_autorizados:
            if not cumple_limite_autorizo(organismo):
                organismo.delete()

    organismos_autorizados = OrganismosAutorizadosRegistrarInterrupto.objects.all()
    nombre_form = "Listado: Organismos autorizados a registrar interruptos fuera del plazo de tiempo establecido."

    return render(request, "Interruptos/OrganismosAutorizados/gestion_organismos_autorizados.html", locals())


@login_required
@permission_required(['administrador'])
def autorizar_organismo(request):

    if request.method == 'POST':
        form = OrganismosAutorizadosRegistrarInterruptoForm(request.POST)

        if 'organismo' in request.POST:
            organismo = request.POST['organismo']

        registrado = OrganismosAutorizadosRegistrarInterrupto.objects.filter(organismo_id=organismo).count()

        if registrado != 0:
            form.add_error('organismo', 'Ya está autorizado este organismo.')

        if form.is_valid():
            organismo_autorizado = form.save(commit=False)
            organismo_autorizado.tiempo_inicia = time.time()
            form.save()
            messages.add_message(request, messages.SUCCESS, "Registrado con éxito.")
            return redirect('/organismos_autorizados')
    else:
        form = OrganismosAutorizadosRegistrarInterruptoForm()
    context = {'form': form, 'nombre_form': "Autorizar al organismo"}
    return render(request, "Interruptos/OrganismosAutorizados/autorizar_organismo.html", context)


@login_required
@permission_required(['administrador'])
def eliminar_organismo_autorizado(request, id_organismo_autorizado):
    organismo_autorizado = OrganismosAutorizadosRegistrarInterrupto.objects.get(id=id_organismo_autorizado)
    organismo_autorizado.delete()
    messages.add_message(request, messages.SUCCESS, "Eliminado con éxito.")
    return redirect('/organismos_autorizados')


def cumple_limite_autorizo(organismo):

    cumple_limite = True

    start = float(organismo.tiempo_inicia)
    end = time.time()
    m, s = divmod(end - start, 60)
    h, m = divmod(m, 60)
    print h
    if h > 48:
        cumple_limite = False

    return cumple_limite
